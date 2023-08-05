#!/usr/bin/env python

import requests
import pickle
from pprint import pprint
import gzip
import xmltodict
from Bio import SeqIO
import tempfile
import pkg_resources


baseUrl = 'http://www.ebi.ac.uk/ena/'
lengthLimit = 100000


def get_data(filename):
    return pkg_resources.resource_filename('enasearch_data', filename)


def load_object(filepath):
    """Load object from a pickle file

    :param filepath: path to pickle file with serialized data
    """
    with open(filepath, 'rb') as f:
        obj = pickle.load(f)
    return obj


results = load_object(get_data("result_description.p"))
filter_types = load_object(get_data("filter_types.p"))
download_options = load_object(get_data("download_options.p"))
display_options = load_object(get_data("display_options.p"))
taxonomy_results = load_object(get_data("taxonomy_results.p"))


def get_results(verbose=True):
    """Return the possible results (type of data) in ENA (other than taxonomy)

    Each result is described in a dictionary with a description of the result,
    the list of returnable fields associated with the result and a dictionnary
    with the filter fields associated with the result

    :param verbose: boolean to define the printing info

    :return: a dictionary with the keys being the result ids and the values dictionary to describe the results
    """
    if verbose:
        for result in results:
            print("%s\t%s" % (result, results[result]["description"]))
    return results


def get_taxonomy_results(verbose=False):
    """Return description about the possible results accessible via the taxon portal.

    Each taxonomy result is described with a short description.

    :param verbose: boolean to define the printing info

    :return: a dictionary with the keys being the result ids and the values dictionary to describe the results
    """
    if verbose:
        pprint(taxonomy_results)
    return taxonomy_results


def check_result(result):
    """Check if a result id is in the list of possible results accessible on ENA

    This function raises an error if the result is not in the list of possible
    results

    :param result: id of result to check
    """
    possible_results = get_results(verbose=False)
    if result not in possible_results:
        err_str = "The result od (%s) does not correspond to a " % (result)
        err_str += "possible result id in ENA"
        raise ValueError(err_str)


def check_taxonomy_result(result):
    """Check if a result id is in the list of possible results in ENA Taxon Portal

    This function raises an error if the result is not in the list of  possible
    taxonomy results

    :param result: id of result to check
    """
    taxonomy_results = get_taxonomy_results(verbose=False)
    if result not in taxonomy_results:
        err_str = "The result id (%s) does not correspond to a " % (result)
        err_str += "possible taxonomy result id in ENA"
        raise ValueError(err_str)


def get_result(result, verbose=False):
    """Return the description of a result (description, returnable and filter fields)

    :param result: id of the result (partition of ENA db), accessible with get_results
    :param verbose: boolean to define the printing info

    :return: dictionary with a description of the result, the list of returnable fields and a dictionnary with the filter fields
    """
    results = get_results(verbose=False)
    check_result(result)
    result_info = results[result]
    if verbose:
        pprint(result_info)
    return result_info


def get_filter_fields(result, verbose=False):
    """Return the filter fields of a result

    This function returns the fields that can be used to build a query on a
    result on ENA. Each field is described in a dictionary with a short
    description and its type (text, number, etc).

    :param result: id of the result (partition of ENA db), accessible with get_results
    :param verbose: boolean to define the printing info

    :return: dictionary with the keys being the fields ids and the values dictionary to describe the fields
    """
    result_info = get_result(result)
    filter_fields = result_info["filter_fields"]
    if verbose:
        pprint(filter_fields)
    return filter_fields


def get_returnable_fields(result, verbose=False):
    """Return the returnable fields of a result

    This function returns the list of fields that can be extracted for a result
    in a query on ENA

    :param result: id of the result (partition of ENA db), accessible with get_results
    :param verbose: boolean to define the printing info

    :return: list of fields that can be extracted for a result
    """
    check_result(result)
    result_info = get_result(result)
    returnable_fields = result_info["returnable_fields"]
    if verbose:
        pprint(returnable_fields)
    return returnable_fields


def check_returnable_fields(fields, result):
    """Check that some field id correspond to returnable fields for a resut

    This function raises an error if one of the ids is not in the list of possible
    returnable fields for the given result

    :param fields: list of fields to check
    :param result: id of the result (partition of ENA db), accessible with get_results
    """
    returnable_fields = get_returnable_fields(result, verbose=False)
    for field in fields:
        if field not in returnable_fields:
            err_str = "The field %s is not a returnable field for " % (field)
            err_str += "result %s" % (result)
            raise ValueError(err_str)


def get_sortable_fields(result, verbose=False):
    """Return the sortable fields of a result

    This function returns the fields that can be used to sort the output of a
    query for a result on ENA. Each field is described in a dictionary with a
    short description and its type (text, number, etc).

    :param result: id of the result (partition of ENA db), accessible with get_results
    :param verbose: boolean to define the printing info

    :return: dictionary with the keys being the fields ids and the values dictionary to describe the fields
    """
    check_result(result)
    sortable_fields = get_filter_fields(result, verbose=False)
    if verbose:
        pprint(sortable_fields)
    return sortable_fields


def check_sortable_fields(fields, result):
    """Check that some field id correspond to sortable fields for a resut

    This function raises an error if one of the ids is not in the list of possible
    sortable fields for the given result

    :param fields: list of fields to check
    :param result: id of the result (partition of ENA db), accessible with get_results
    """
    sortable_fields = get_sortable_fields(result, verbose=False)
    for field in fields:
        if field not in sortable_fields:
            err_str = "The field %s is not a sortable field for " % (field)
            err_str += "result %s" % (result)
            raise ValueError(err_str)


def get_filter_types(verbose=False):
    """Return the filters that can be used for the different type of data in a query on ENA

    This function returns the filters that can be used for the different type of
    data (information available with the information on the filter fileds). For
    each type of data is given the operations applicable and a description of the
    type of expected values

    :param result: id of the result (partition of ENA db), accessible with get_results
    :param verbose: boolean to define the printing info

    :return: dictionary with the keys being the type of data and the values dictionary to describe the filters for this type of data
    """
    if verbose:
        pprint(filter_types)
    return filter_types


def get_display_options(verbose=False):
    """Return the possible formats to display the result of a query on ENA

    :param verbose: boolean to define the printing info

    :return: dictionary with the keys being the formats and the values a description of the formats
    """
    if verbose:
        pprint(display_options)
    return display_options


def check_display_option(display):
    """Check if a display id is in the list of output formats for a query on ENA

    This function raises an error if the id is not in the list of possible
    displayable format

    :param display: display to check
    """
    display_options = get_display_options(verbose=False)
    if display not in display_options:
        err_str = "The display value (%s) does not correspond to a possible \
        display value in ENA" % (display)
        raise ValueError(err_str)


def get_download_options(verbose=False):
    """Return the options for download of data from ENA

    :param verbose: boolean to define the printing info

    :return: dictionary with the options and the values a description of the options
    """
    if verbose:
        pprint(download_options)
    return download_options


def check_download_option(download):
    """Check if an options is in the list of options for download of data from ENA

    This function raises an error if the id is not in the list of possible
    download options

    :param download: download format to check
    """
    download_options = get_download_options(verbose=False)
    if download not in download_options:
        err_str = "The download value does not correspond to a possible "
        err_str += "display value in ENA"
        raise ValueError(err_str)


def check_length(length):
    """Check if length (number of results for a query) is below the maximum

    This function raises an error if the given length (or number of results for
    a query) is below the maximum value <lengthLimit>

    :param length: length value to test
    """
    if length > lengthLimit:
        err_str = "The length value (%s) is higher than the " % (length)
        err_str += "limit length (%s)" % (lengthLimit)
        raise ValueError(err_str)


def check_download_file_options(download, file):
    """Check that download and file options are correctly defined

    This function check:

    - A filepath is given
    - A download option is given
    - The download option is in the list of options for download of data from ENA

    :param download: download option to specify that records are to be saved in a file (used with file option, accessible with get_download_options)
    :param file: filepath to save the content of the data (used with download option)
    """
    if file is None:
        err_str = "download option should come along with a filepath"
        raise ValueError(err_str)
    if download is None:
        err_str = "file option should come along with a download option"
        raise ValueError(err_str)
    check_download_option(download)


def check_subseq_range(subseq_range):
    """Check that a range of sequences to extract is well defined

    This function check:

    - The range is correctly built: 2 integer values separated by a -
    - The second value is higher than the first one

    :param download: range for subsequences (limit separated by a -)
    """
    subseq_range_content = subseq_range.split("-")
    if len(subseq_range_content) != 2:
        err_str = "A subseq_range must have two arguments (start and stop)"
        err_str += " separated by a -"
        raise ValueError(err_str)
    if int(subseq_range_content[0]) > int(subseq_range_content[1]):
        err_str = "Start for a subseq_range must be lower than the stop"
        raise ValueError(err_str)


def format_seq_content(seq_str, out_format):
    """Format a string with sequences into a list of BioPython sequence objects (SeqRecord)

    :param seq_str: string with sequences to format
    :param out_format: fasta or fastq

    :return: a list of SeqRecord objects with the sequences in the input string
    """
    sequences = []
    with tempfile.TemporaryFile(mode='w+') as fp:
        fp.write(seq_str)
        fp.seek(0)
        for record in SeqIO.parse(fp, out_format):
            sequences.append(record)
    return sequences


def request_url(url, display, file=None):
    """Run the URL request and return content or status

    This function tooks an URL built to query or extract data from ENA and apply
    this URL. If a filepath is given, the function puts the result into the
    file and returns the status of the request. Otherwise, the results of the
    request is returned by the function in different format depending of the
    display format

    :param url: URL to request on ENA
    :param display: display option
    :param length: number of records to retrieve
    :param file: filepath to save the content of the search

    :return: status of the request or the result of the request (in different format)
    """
    if file is not None:
        r = requests.get(url, stream=True)
        r.raise_for_status()
        with open(file, "wb") as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)
        return r.raise_for_status()
    else:
        r = requests.get(url)
        r.raise_for_status()
        if display == "xml":
            return xmltodict.parse(r.text)
        elif display == "fasta" or display == "fastq":
            return format_seq_content(r.text, display)
        else:
            return r.text


def build_retrieve_url(
    ids, display, result=None, download=None, file=None, offset=None,
    length=None, subseq_range=None, expanded=False, header=False
):
    """Build the URL to retrieve data or taxon

    This function builds the URL to retrieve data or taxon on ENA. It takes
    several arguments, check their validity before combining them to build the
    URL.

    :param ids: comma-separated identifiers for records other than Taxon
    :param display: display option to specify the display format (accessible with get_display_options)
    :param offset: first record to get
    :param length: number of records to retrieve
    :param download: download option to specify that records are to be saved in a file (used with file option, accessible with get_download_options)
    :param file: filepath to save the content of the search (used with download option)
    :param subseq_range: range for subsequences (limit separated by a -)
    :param expanded: boolean to determine if a CON record is expanded
    :param header: boolean to obtain only the header of a record

    :return: a string with the build URL
    """
    url = baseUrl + "data/view/"
    url += ids
    check_display_option(display)
    url += "&display=%s" % (display)
    if result is not None:
        url += "&result=%s" % (result)
    if length is not None:
        check_length(length)
        url += "&length=%s" % (length)
    if offset is not None:
        url += "&offset=%s" % (offset)
    if subseq_range is not None:
        check_subseq_range(subseq_range)
        url += "&range=%s" % (subseq_range)
    url += "&expanded=true" if expanded else "&expanded=false"
    url += "&header=true" if header else "&header=false"
    if download is not None or file is not None:
        check_download_file_options(download, file)
        url += "&download=%s" % (download)
    return url


def retrieve_data(
    ids, display, download=None, file=None, offset=None, length=None,
    subseq_range=None, expanded=False, header=False
):
    """Retrieve ENA data (other than taxon)

    This function retrieves data (other than taxon) from ENA by:

    - Building the URL based on the ids to retrieve and some parameters to format the results
    - Requesting the URL to extract the data

    :param ids: comma-separated identifiers for records other than Taxon
    :param display: display option to specify the display format (accessible with get_display_options)
    :param offset: first record to get
    :param length: number of records to retrieve
    :param download: download option to specify that records are to be saved in a file (used with file option, accessible with get_download_options)
    :param file: filepath to save the content of the search (used with download option)
    :param subseq_range: range for subsequences (limit separated by a -)
    :param expanded: boolean to determine if a CON record is expanded
    :param header: boolean to obtain only the header of a record

    :return: data corresponding to the requested ids and formatted given the parameters
    """
    url = build_retrieve_url(
        ids=ids,
        display=display,
        result=None,
        download=download,
        file=file,
        offset=offset,
        length=length,
        subseq_range=subseq_range,
        expanded=expanded,
        header=header)
    return request_url(url, display, file)


def retrieve_taxons(
    ids, display, result=None, download=None, file=None, offset=None,
    length=None, subseq_range=None, expanded=False, header=False
):
    """Retrieve data from the ENA Taxon Portal

    This function retrieves data (other than taxon) from ENA by:

    - Formatting the ids to query then on the Taxon Portal
    - Building the URL based on the ids to retrieve and some parameters to format the results
    - Requesting the URL to extract the data

    :param ids: comma-separated taxon identifiers
    :param display: display option to specify the display format (accessible with get_display_options)
    :param result: taxonomy result to display (accessible with result)
    :param offset: first record to get
    :param length: number of records to retrieve
    :param download: download option to specify that records are to be saved in a file (used with file option, accessible with get_download_options)
    :param file: filepath to save the content of the search (used with download option)
    :param subseq_range: range for subsequences (limit separated by a -)
    :param expanded: boolean to determine if a CON record is expanded
    :param header: boolean to obtain only the header of a record

    :return: data corresponding to the requested ids and formatted given the parameters
    """
    id_list = ids.split(",")
    modified_ids = []
    for one_id in id_list:
        modified_ids.append("Taxon:%s" % (one_id))
    if result is not None:
        check_taxonomy_result(result)
    url = build_retrieve_url(
        ids=",".join(modified_ids),
        display=display,
        result=result,
        download=download,
        file=file,
        offset=offset,
        length=length,
        subseq_range=subseq_range,
        expanded=expanded,
        header=header)
    return request_url(url, display, file)


def get_search_url(free_text_search):
    """Get the prefix for the URL to search ENA database

    :param free_text_search: boolean to describe the type of query

    :return: a string with the prefix of an URL to search ENA database
    """
    url = baseUrl + "data/"
    if not free_text_search:
        url += "warehouse/"
    url += "search?"
    return url


def get_search_result_number(
    free_text_search, query, result, need_check_result=True
):
    """Get the number of results for a query on a result

    This function builds a query on ENA to extract the number of results
    matching the query on ENA

    :param free_text_search: boolean to describe the type of query
    :param query: query string, made up of filtering conditions, joined by logical ANDs, ORs and NOTs and bound by double quotes
    :param result: id of the result (partition of ENA db), accessible with get_results

    :return: an integer corresponding to the number of results of a query on ENA
    """
    url = get_search_url(free_text_search)
    url += "query=%s" % (query)

    if need_check_result:
        check_result(result)
    url += "&result=%s" % (result)

    url += "&resultcount"
    r = requests.get(
        url,
        headers={"accept": "application/json"})
    r.raise_for_status()
    nb = r.text.split("\n")[0].split(": ")[1].replace(",", "")
    return int(nb)


def search_data(
    free_text_search, query, result, display, offset=None, length=None,
    download=None, file=None, fields=None, sortfields=None
):
    """Search ENA data

    This function

    - Builds the URL for a given query to search/extract data on ENA database
    - Formats the results given the option defined

    The number of results for the query is limited at <lengthLimit>

    :param free_text_search: boolean to describe the type of query
    :param query: query string, made up of filtering conditions, joined by logical ANDs, ORs and NOTs and bound by double quotes
    :param result: id of the result (partition of ENA db), accessible with get_results
    :param display: display option to specify the display format (accessible with get_display_options)
    :param offset: first record to get
    :param length: number of records to retrieve
    :param download: download option to specify that records are to be saved in a file (used with file option)
    :param file: filepath to save the content of the search (used with download option)
    :param fields: comma-separated list of fields to return (only if display=report)
    :param sortfields: comma-separated list of fields to sort the results (only if display=report)

    :return: results of the request in a format defined in the parameters
    """
    url = get_search_url(free_text_search)
    url += "query=%s" % (query)

    check_result(result)
    url += "&result=%s" % (result)

    check_display_option(display)
    url += "&display=%s" % (display)

    if length is not None:
        check_length(length)
        url += "&length=%s" % (length)

    if offset is not None:
        result_nb = get_search_result_number(free_text_search, query, result)
        if offset > result_nb:
            err_str = "The offset value must be lower than the possible number"
            err_str += " of results for the query"
            raise ValueError(err_str)
        url += "&offset=%s" % (offset)

    if display == "report":
        if fields is None:
            fields = ",".join(get_returnable_fields(result))
        else:
            check_returnable_fields(fields.split(","), result)
        url += "&fields=%s" % (fields)
        if sortfields is not None:
            check_sortable_fields(sortfields, result)
            url += "&sortfields=%s" % (sortfields)

    if download is not None or file is not None:
        check_download_file_options(download, file)
        url += "&download=%s" % (download)
    return request_url(url, display, file)


def search_all_data(
    free_text_search, query, result, display, download=None, file=None
):
    """Search ENA data and get all results (not size limited)

    This function

    - Extracts the number of possible results for the query
    - Extracts the all the results of the query (by potentially running several
      times the search function)

    :param free_text_search: boolean to describe the type of query
    :param query: query string, made up of filtering conditions, joined by logical ANDs, ORs and NOTs and bound by double quotes
    :param result: id of the result (partition of ENA db), accessible with get_results
    :param display: display option to specify the display format
    :param download: download option to specify that records are to be saved in a file (used with file option)
    :param file: filepath to save the content of the search (used with download option)

    :return: all results of the request in a format defined in the parameters
    """
    if display not in ["fasta", "fastq"]:
        err_str = "This function is not possible for this display option"
        raise ValueError(err_str)

    if download is not None or file is not None:
        check_download_file_options(download, file)

    result_nb = get_search_result_number(free_text_search, query, result)
    quotient = int(result_nb / float(lengthLimit))
    start = 0
    all_results = []
    for i in range(quotient):
        start = lengthLimit * i
        all_results += search_data(
            free_text_search=free_text_search,
            query=query,
            result=result,
            display=display,
            offset=start,
            length=lengthLimit,
            fields=None,
            sortfields=None)
    if (result_nb % lengthLimit) > 0:
        if quotient > 0:
            start = lengthLimit * quotient
            remainder = result_nb - start
        else:
            start = None
            remainder = None
        all_results += search_data(
            free_text_search=free_text_search,
            query=query,
            result=result,
            display=display,
            offset=start,
            length=remainder,
            fields=None,
            sortfields=None)
    if file:
        if display in ['fasta', 'fastq']:
            SeqIO.write(all_results, file, display)
            if download == "gzip":
                with open(file, "r") as fd:
                    all_results = fd.read()
                with gzip.open(file, 'wb') as fd:
                    fd.write(all_results)
        elif download == "gzip":
            with gzip.open(file, 'wb') as fd:
                fd.write(all_results)
        else:
            with open(file, "w") as fd:
                fd.write(all_results)
    else:
        return all_results


def retrieve_filereport(accession, result, fields=None, file=None):
    """Retrieve a file (run or analysis) report

    This function builds an URL to retrieve file (run or analysis) report from
    ENA and return the result of the request.

    :param accession: accession id
    :param result: read_run for a run report or analysis for an analysis report
    :param fields: comma-separated list of fields to have in the report
    :param file: filepath to save the content of the report

    :return: requested file report
    """
    url = baseUrl + "data/warehouse/filereport?"
    url += "accession=%s" % (accession)

    if result not in ["read_run", "analysis"]:
        err_str = "The result to retrieve a filereport must be either read_run"
        err_str += " or analysis"
        raise ValueError(err_str)
    url += "&result=%s" % (result)

    if fields is None:
        fields = ",".join(get_returnable_fields(result))
    else:
        check_returnable_fields(fields.split(","), result)
    url += "&fields=%s" % (fields)

    return request_url(url, "text", file)


def retrieve_run_report(accession, fields=None, file=None):
    """Retrieve run report from ENA

    :param accession: accession id
    :param fields: comma-separated list of fields to have in the report (accessible with get_returnable_fields with result=read_run)
    :param file: filepath to save the content of the report

    :return: requested run report
    """
    return retrieve_filereport(
        accession=accession,
        result="read_run",
        fields=fields,
        file=file)


def retrieve_analysis_report(accession, fields=None, file=None):
    """Retrieve analysis report from ENA

    :param accession: accession id
    :param fields: comma-separated list of fields to have in the report (accessible with get_returnable_fields with result=analysis)
    :param file: filepath to save the content of the report

    :return: requested run repor
    """
    return retrieve_filereport(
        accession=accession,
        result="analysis",
        fields=fields,
        file=file)
