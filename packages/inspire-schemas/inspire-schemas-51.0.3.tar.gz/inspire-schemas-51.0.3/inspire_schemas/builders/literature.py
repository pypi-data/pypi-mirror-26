# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE-SCHEMAS.
# Copyright (C) 2017 CERN.
#
# INSPIRE-SCHEMAS is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# INSPIRE-SCHEMAS is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with INSPIRE-SCHEMAS; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Literature builder class and related code."""

from __future__ import absolute_import, division, print_function

import warnings
from functools import wraps

import idutils

from ..utils import (get_license_from_url,
                     normalize_author_name,
                     normalize_collaboration,
                     validate)

EMPTIES = [None, '', [], {}]


def filter_empty_parameters(func):
    """Decorator that is filtering empty parameters.

    :param func: function that you want wrapping
    :type func: function
    """
    @wraps(func)
    def func_wrapper(self, *args, **kwargs):
        my_kwargs = {key: value for key, value in kwargs.items()
                     if value not in EMPTIES}

        if (
                {'source', 'material'}.issuperset(my_kwargs) or not my_kwargs
        ) and args == ():
            return
        return func(self, *args, **my_kwargs)

    return func_wrapper


def is_citeable(publication_info):
    """Check some fields in order to define if the article is citeable.

    :param publication_info: publication_info field
    already populated
    :type publication_info: list
    """
    def _item_has_pub_info(item):
        return all(
            key in item for key in (
                'journal_title', 'journal_volume'
            )
        )

    def _item_has_page_or_artid(item):
        return any(
            key in item for key in (
                'page_start', 'artid'
            )
        )

    has_pub_info = any(
        _item_has_pub_info(item) for item in publication_info
    )
    has_page_or_artid = any(
        _item_has_page_or_artid(item) for item in publication_info
    )

    return has_pub_info and has_page_or_artid


class LiteratureBuilder(object):
    """Literature record builder."""

    def __init__(self, source=None, record=None):
        """Init method.

        :param source: sets the default value for the 'source' fields
         of the current record, which captures where the information
         that the builder populates comes from
        :type source: string

        :param record: sets the default value for the the current
        record, in order to edit an already existent record
        :type record: dict
        """
        if record is None:
            self.record = {
                '_collections': ['Literature'],
                'curated': False,
            }
        else:
            self.record = record

        self.source = source

    def _append_to(self, field, element):
        """Append the ``element`` to the ``field`` of the record.

        This method is smart: it does nothing if ``element`` is empty and
        creates ``field`` if it does not exit yet.

        :param field: the name of the field of the record to append to
        :type field: string
        :param element: the element to append
        """
        if element not in EMPTIES:
            self.record.setdefault(field, [])
            self.record.get(field).append(element)

    def __str__(self):
        """Print the current record."""
        return str(self.record)

    def __repr__(self):
        """Printable representation of the builder."""
        return 'LiteratureBuilder(source="{}", record={})'.format(
            self.source,
            self.record
        )

    def _sourced_dict(self, source=None, **kwargs):
        """Like ``dict(**kwargs)``, but where the ``source`` key is special.
        """
        if source:
            kwargs['source'] = source
        elif self.source:
            kwargs['source'] = self.source
        return kwargs

    def validate_record(self):
        """Validate the record in according to the hep schema."""
        validate(self.record, 'hep')

    @filter_empty_parameters
    def add_abstract(self, abstract, source=None):
        """Add abstract.

        :param abstract: abstract for the current document.
        :type abstract: string

        :param source: source for the given abstract.
        :type source: string
        """
        self._append_to('abstracts', self._sourced_dict(
            source,
            value=abstract.strip(),
        ))

    @filter_empty_parameters
    def add_arxiv_eprint(self, arxiv_id, arxiv_categories):
        """Add arxiv eprint.

        :param arxiv_id: arxiv id for the current document.
        :type arxiv_id: string

        :param arxiv_categories: arXiv categories for the current document.
        :type arxiv_categories: list
        """
        self._append_to('arxiv_eprints', {
            'value': arxiv_id,
            'categories': arxiv_categories,
        })
        self.set_citeable(True)

    @filter_empty_parameters
    def add_doi(self, doi, source=None, material=None):
        """Add doi.

        :param doi: doi for the current document.
        :type doi: string

        :param source: source for the doi.
        :type source: string

        :param material: material for the doi.
        :type material: string
        """
        doi = idutils.normalize_doi(doi)
        if not doi:
            return

        dois = self._sourced_dict(
            source,
            value=doi
        )
        if material is not None:
            dois['material'] = material

        self._append_to('dois', dois)

    @filter_empty_parameters
    def add_author(self, author):
        """Add author.

        :param author: author for a given document
        :type author: object that make_author method
        produces
        """
        self._append_to('authors', author)

    @filter_empty_parameters
    def make_author(self, full_name,
                    affiliations=None,
                    roles=None,
                    raw_affiliations=None,
                    source=None,
                    ids=None,
                    emails=None,
                    alternative_names=None):
        """Make a subrecord representing an author.

        Args:
            full_name(str): full name of the author. If not yet in standard
                Inspire form, it will be normalized.
            affiliations(List[str]): Inspire normalized affiliations of the
                author.
            roles(List[str]): Inspire roles of the author.
            raw_affiliations(List[str]): raw affiliation strings of the author.
            source(str): source for the affiliations when
                ``affiliations_normalized`` is ``False``.
            ids(List[Tuple[str,str]]): list of ids of the author, whose
                elements are of the form ``(schema, value)``.
            emails(List[str]): email addresses of the author.
            alternative_names(List[str]): alternative names of the author.

        Returns:
            dict: a schema-compliant subrecord.
        """
        def _add_affiliations(author, affiliations):
            if affiliations is None:
                return

            author.setdefault('affiliations', [])
            for affiliation in filter(bool, affiliations):
                author['affiliations'].append({
                    'value': affiliation
                })

        def _add_raw_affiliations(author, raw_affiliations, source):
            if raw_affiliations is None:
                return

            author.setdefault('raw_affiliations', [])
            for raw_affiliation in filter(bool, raw_affiliations):
                author['raw_affiliations'].append(self._sourced_dict(
                    source,
                    value=raw_affiliation,
                ))

        def _add_emails(author, emails):
            if emails is None:
                return

            author.setdefault('emails', []).extend(filter(bool, emails))

        def _add_ids(author, ids):
            if ids is None:
                return

            author.setdefault('ids', [])
            for schema, value in ids:
                if value:
                    author['ids'].append({
                        'schema': schema,
                        'value': value,
                    })

        def _add_alternative_names(author, alternative_names):
            if alternative_names is None:
                return

            author.setdefault('alternative_names', []).extend(
                filter(bool, alternative_names)
            )

        def _add_inspire_roles(author, inspire_roles):
            if inspire_roles is None:
                return

            author.setdefault('inspire_roles', []).extend(filter(bool, roles))

        author = {}

        author['full_name'] = normalize_author_name(full_name)

        _add_affiliations(author, affiliations)
        _add_raw_affiliations(author, raw_affiliations, source)
        _add_emails(author, emails)
        _add_ids(author, ids)
        _add_alternative_names(author, alternative_names)
        _add_inspire_roles(author, roles)

        return author

    @filter_empty_parameters
    def add_book(self, publisher=None, place=None, date=None):
        """
        Make a dictionary that is representing a book.

        :param publisher: publisher name

        :type publisher: string

        :param place: place of publication
        :type place: string

        :param date: the date of publication
        :type date: date

        :rtype: dict
        """

        imprint = {}
        if date is not None:
            imprint['date'] = date
        if place is not None:
            imprint['place'] = place
        if publisher is not None:
            imprint['publisher'] = publisher

        self._append_to('imprints', imprint)

    @filter_empty_parameters
    def add_isbn(self, isbn, medium=None):
        """
        :param isbns: the isbns of the book
        :type isbns: object
        """
        isbn_dict = {}
        if isbn is not None:
            isbn_dict['value'] = isbn
        if medium is not None:
            isbn_dict['medium'] = medium

        self._append_to('isbns', isbn_dict)

    @filter_empty_parameters
    def add_book_series(self, title, volume=None):
        """
        :param volume: the volume of the book
        :type volume: string

        :param title: the title of the book
        :type title: string
        """
        book_series = {}
        if title is not None:
            book_series['title'] = title
        if volume is not None:
            book_series['volume'] = volume

        self._append_to('book_series', book_series)

    @filter_empty_parameters
    def add_book_edition(self, edition):
        """
        :param edition: the edition of the book
        :type edition: string
        """
        self._append_to('editions', edition)

    @filter_empty_parameters
    def add_inspire_categories(self, subject_terms, source=None):
        """Add inspire categories.

        :param subject_terms: user categories for the current document.
        :type subject_terms: list

        :param source: source for the given categories.
        :type source: string
        """
        for category in subject_terms:
            category_dict = self._sourced_dict(
                source,
                term=category,
            )
            self._append_to('inspire_categories', category_dict)

    @filter_empty_parameters
    def add_keyword(self, keyword, schema=None, source=None):
        """Add a keyword.

        Args:
            keyword(str): keyword to add.
            schema(str): schema to which the keyword belongs.
            source(str): source for the keyword.
        """
        keyword_dict = self._sourced_dict(source, value=keyword)

        if schema is not None:
            keyword_dict['schema'] = schema

        self._append_to('keywords', keyword_dict)

    @filter_empty_parameters
    def add_private_note(self, private_notes, source=None):
        """Add private notes.

        :param private_notes: hidden notes for the current document
        :type private_notes: string

        :param source: source for the given private notes
        :type source: string
        """
        self._append_to('_private_notes', self._sourced_dict(
            source,
            value=private_notes,
        ))

    @filter_empty_parameters
    def add_publication_info(
        self,
        year=None,
        cnum=None,
        artid=None,
        page_end=None,
        page_start=None,
        journal_issue=None,
        journal_title=None,
        journal_volume=None,
        pubinfo_freetext=None,
        material=None,
        parent_record=None,
    ):
        """Add publication info.

        :param year: year of publication
        :type year: integer

        :param cnum: inspire conference number
        :type cnum: string

        :param artid: article id
        :type artid: string

        :param page_end: final page for the article
        :type page_end: string

        :param page_start: initial page for the article
        :type page_start: string

        :param journal_issue: issue of the journal where
        the document has been published
        :type journal_issue: string

        :param journal_title: title of the journal where
        the document has been published
        :type journal_title: string

        :param journal_volume: volume of the journal where
        the document has been published
        :type journal_volume: string

        :param pubinfo_freetext: Unstructured text describing the publication
        information.
        :type pubinfo_freetext: string

        :param material: material of the article
        :type material: string

        :param parent_record: reference for the parent record
        :type parent_record: string
        """
        publication_item = {}
        for key in ('cnum', 'artid', 'page_end', 'page_start',
                    'journal_issue', 'journal_title',
                    'journal_volume', 'year', 'pubinfo_freetext', 'material'):
            if locals()[key] is not None:
                publication_item[key] = locals()[key]
        if parent_record is not None:
            parent_item = {'$ref': parent_record}
            publication_item['parent_record'] = parent_item
        if page_start and page_end:
            try:
                self.add_number_of_pages(
                    int(page_end) - int(page_start) + 1
                )
            except (TypeError, ValueError):
                pass

        self._append_to('publication_info', publication_item)

        if is_citeable(self.record['publication_info']):
            self.set_citeable(True)

    @filter_empty_parameters
    def add_imprint_date(self, imprint_date):
        """Add imprint date.

        :type imprint_date: string. A formatted date is required (yyyy-mm-dd)
        """
        self._append_to('imprints', {
            'date': imprint_date
        })

    @filter_empty_parameters
    def add_preprint_date(self, preprint_date):
        """Add preprint date.

        :type preprint_date: string. A formatted date is required (yyyy-mm-dd)
        """
        self.record['preprint_date'] = preprint_date

    @filter_empty_parameters
    def add_thesis(
        self,
        defense_date=None,
        degree_type=None,
        institution=None,
        date=None
    ):
        """Add thesis info.

        :param defense_date: defense date for the current thesis
        :type defense_date: string. A formatted date is required (yyyy-mm-dd)

        :param degree_type: degree type for the current thesis
        :type degree_type: string

        :param institution: author's affiliation for the current thesis
        :type institution: string

        :param date: publication date for the current thesis
        :type date: string. A formatted date is required (yyyy-mm-dd)
        """
        self.record.setdefault('thesis_info', {})

        thesis_item = {}
        for key in ('defense_date', 'date'):
            if locals()[key] is not None:
                thesis_item[key] = locals()[key]

        if degree_type is not None:
            thesis_item['degree_type'] = degree_type.lower()

        if institution is not None:
            thesis_item['institutions'] = [{'name': institution}]

        self.record['thesis_info'] = thesis_item

    @filter_empty_parameters
    def add_accelerator_experiments_legacy_name(self, legacy_name):
        """Add legacy name in accelerator experiment.

        :type legacy_name: string
        """
        self._append_to('accelerator_experiments', {
            'legacy_name': legacy_name
        })

    @filter_empty_parameters
    def add_language(self, language):
        """Add language.

        :param language: language for the current document
        :type language: string (2 characters ISO639-1)
        """
        self._append_to('languages', language)

    @filter_empty_parameters
    def add_license(
        self,
        url=None,
        license=None,
        material=None,
        imposing=None
    ):
        """Add license.

        :param url: url for the description of the license
        :type url: string

        :param license: license type
        :type license: string

        :param material: material type
        :type material: string

        :param imposing: imposing type
        :type imposing: string
        """
        hep_license = {}

        try:
            license = get_license_from_url(url)
        except ValueError:
            pass

        for key in ('url', 'license', 'material', 'imposing'):
            if locals()[key] is not None:
                hep_license[key] = locals()[key]

        self._append_to('license', hep_license)

    @filter_empty_parameters
    def add_public_note(self, public_note, source=None):
        """Add public note.

        :param public_note: public note for the current article.
        :type public_note: string

        :param source: source for the given notes.
        :type source: string
        """
        self._append_to('public_notes', self._sourced_dict(
            source,
            value=public_note,
        ))

    @filter_empty_parameters
    def add_title(self, title, subtitle=None, source=None):
        """Add title.

        :param title: title for the current document
        :type title: string

        :param subtitle: subtitle for the current document
        :type subtitle: string

        :param source: source for the given title
        :type source: string
        """
        title_entry = self._sourced_dict(
            source,
            title=title,
        )
        if subtitle is not None:
            title_entry['subtitle'] = subtitle

        self._append_to('titles', title_entry)

    @filter_empty_parameters
    def add_title_translation(self, title, language=None, source=None):
        """Add title translation.

        :param title: translated title
        :type title: string

        :param language: language for the original title
        :type language: string (2 characters ISO639-1)

        :param source: source for the given title
        :type source: string
        """
        title_translation = self._sourced_dict(
            source,
            title=title,
        )
        if language is not None:
            title_translation['language'] = language

        self._append_to('title_translations', title_translation)

    @filter_empty_parameters
    def add_url(self, url):
        """Add url.

        :param url: url for additional information for the current document
        :type url: string
        """
        self._append_to('urls', {
            'value': url
        })

    @filter_empty_parameters
    def add_report_number(self, report_number, source=None):
        """Add report numbers.

        :param report_number: report number for the current document
        :type report_number: string

        :param source: source for the given report number
        :type source: string
        """
        self._append_to('report_numbers', self._sourced_dict(
            source,
            value=report_number,
        ))

    @filter_empty_parameters
    def add_collaboration(self, collaboration):
        """Add collaboration.

        :param collaboration: collaboration for the current document
        :type collaboration: string
        """
        collaborations = normalize_collaboration(collaboration)
        for collaboration in collaborations:
            self._append_to('collaborations', {
                'value': collaboration
            })

    @filter_empty_parameters
    def add_acquisition_source(
        self,
        method,
        date=None,
        submission_number=None,
        internal_uid=None,
        email=None,
        orcid=None,
        source=None,
        datetime=None,
    ):
        """Add acquisition source.

        :type submission_number: integer

        :type email: integer

        :type source: string

        :param date: UTC date in isoformat

                     .. deprecated:: 30.1.0
                        Use ``datetime`` instead.
        :type date: string

        :param method: method of acquisition for the suggested document
        :type method: string

        :param orcid: orcid of the user that is creating the record
        :type orcid: string

        :param internal_uid: id of the user that is creating the record
        :type internal_uid: string

        :param datetime: UTC datetime in ISO 8601 format
        :type datetime: string
        """
        if date is not None:
            if datetime is not None:
                raise ValueError("Conflicting args: 'date' and 'datetime'")
            warnings.warn("Use 'datetime', not 'date'", DeprecationWarning)
            datetime = date

        acquisition_source = self._sourced_dict(source)

        acquisition_source['submission_number'] = str(submission_number)
        for key in ('datetime', 'email', 'method', 'orcid', 'internal_uid'):
            if locals()[key] is not None:
                acquisition_source[key] = locals()[key]

        self.record['acquisition_source'] = acquisition_source

    @filter_empty_parameters
    def add_document_type(self, document_type):
        """Add document type.

        :type document_type: string
        """
        self._append_to('document_type', document_type)

    @filter_empty_parameters
    def add_copyright(
        self,
        material=None,
        holder=None,
        statement=None,
        url=None,
        year=None
    ):
        """Add Copyright.

        :type material: string

        :type holder: string

        :type statement: string

        :type url: string

        :type year: int
        """
        copyright = {}
        for key in ('holder', 'statement', 'url'):
            if locals()[key] is not None:
                copyright[key] = locals()[key]

        if material is not None:
            copyright['material'] = material.lower()

        if year is not None:
            copyright['year'] = int(year)

        self._append_to('copyright', copyright)

    @filter_empty_parameters
    def add_number_of_pages(self, number_of_pages):
        """Add number_of_pages.

        :type number_of_pages: integer
        """
        self.record['number_of_pages'] = number_of_pages

    @filter_empty_parameters
    def add_collection(self, collection):
        """Add collection.

        :param collection: defines the type of the current document
        :type collection: string
        """
        self._append_to('_collections', collection)

    @filter_empty_parameters
    def add_publication_type(self, publication_type):
        """Add publication_type.

        :param publication_type: Defines the type
        of the current document
        :type publication_type: string
        """
        self._append_to('publication_type', publication_type)

    def set_core(self, core=True):
        """Set core flag.

        :param core: define a core article
        :type core: bool
        """
        self.record['core'] = core

    def set_refereed(self, refereed=True):
        """Set refereed flag.

        :param refereed: define a refereed article
        :type refereed: bool
        """
        self.record['refereed'] = refereed

    def set_withdrawn(self, withdrawn=True):
        """Set withdrawn flag.

        :param withdrawn: define a withdrawn article
        :type withdrawn: bool
        """
        self.record['withdrawn'] = withdrawn

    def set_citeable(self, citeable=True):
        """Set citeable flag.

        :param citeable: define a citeable article
        :type citeable: bool
        """
        self.record['citeable'] = citeable

    def set_curated(self, curated=True):
        """Set curated flag."""
        self.record['curated'] = curated

    @filter_empty_parameters
    def add_figure(
        self,
        key,
        caption=None,
        label=None,
        material=None,
        source=None,
        url=None,
    ):
        """Add a figure."""
        figure = self._sourced_dict(source)

        if key:
            figure['key'] = key

        for key in ('caption', 'label', 'material', 'url'):
            if locals()[key] is not None:
                figure[key] = locals()[key]

        if figure:
            self._append_to('figures', figure)

    @filter_empty_parameters
    def add_document(
        self,
        key,
        description=None,
        fulltext=None,
        hidden=None,
        material=None,
        original_url=None,
        source=None,
        url=None,
    ):
        """Add a document."""
        document = self._sourced_dict(source)

        if key:
            document['key'] = key

        for key in (
            'description',
            'fulltext',
            'hidden',
            'material',
            'original_url',
            'url',
        ):
            if locals()[key] is not None:
                document[key] = locals()[key]

        if document:
            self._append_to('documents', document)
