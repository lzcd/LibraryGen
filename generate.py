#!/usr/bin/python3

from enum import Enum
import os
import sys
import getopt
from pathlib import Path
import subprocess
import urllib.request
import json


class Options:
    def __init__(self) -> None:
        self.ignore_existing_directories = True
        self.generate_pngs = True
        self.extract_text = True
        self.generate_jpgs = True
        self.cleanup_pngs = True
        self.generate_pdf_structures = True
        self.generate_pdf_searchs = True
        self.generate_structure = True
        self.preserve_existing_meta = True
        self.generate_meta_from_isbn = True
        self.generate_meta_from_text = True
        self.cleanup_txts = True
        self.input_root_path = "test-input"
        self.output_root_path = "test-output"


class Meta:
    def __init__(self) -> None:
        self.isbn = ""
        self.authors = list[str]()
        self.title = ""
        self.thumbnail_url = ""


class RunnerResult:
    def __init__(self) -> None:
        self.output_text = None
        self.error_text = None

    def stuff() -> None:
        pass


class Runner:
    def __init__(self) -> None:
        pass

    def execute(self, line: list[str]) -> RunnerResult:
        process_result = subprocess.run(
            line, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        result = RunnerResult()
        result.output_text = process_result.stdout.decode("utf-8")
        result.error_text = process_result.stderr.decode("utf-8")
        return result


class Extractor:
    def __init__(self) -> None:
        pass

    def extract(
        self, options: Options, pdf_file_path: str, output_folder_path: str
    ) -> None:
        if options.generate_pngs:
            self.generate_png_files(pdf_file_path, output_folder_path)
            
        png_stem_names = self.find_png_stem_names(output_folder_path)

        page_png_stem_names = list[str]()
        for png_stem_index in range(len(png_stem_names)):
            page_png_stem_name = "".join(["page", str(png_stem_index).zfill(4)])
            page_png_stem_names.append(page_png_stem_name)

            human_page_name = "".join(["page ", str(png_stem_index + 1)])

            
            if options.extract_text:
                print("".join(["Extracting text from ", human_page_name]))

                png_stem_name = png_stem_names[png_stem_index]
                png_file_name = "".join([png_stem_name, ".png"])

                input_png_path = os.path.join(output_folder_path, png_file_name)
                output_txt_path = os.path.join(output_folder_path, page_png_stem_name)

                self.generate_bordered_png_file(output_folder_path, page_png_stem_name, input_png_path)

                bordered_png_file_name = "".join([page_png_stem_name, ".bordered.png"])
                bordered_png_path = os.path.join(output_folder_path, bordered_png_file_name)

                self.extract_txt_file(bordered_png_path, output_txt_path)

            if options.generate_jpgs:
                print("".join(["Optimising image from ", human_page_name]))
                self.generate_jpg_file(
                    output_folder_path, page_png_stem_name, input_png_path
                )

        if options.cleanup_pngs:
            for png_stem_index in range(len(png_stem_names)):
                human_page_name = "".join(["page ", str(png_stem_index + 1)])
                print("".join(["Cleaning up image for ", human_page_name]))
                png_stem_name = png_stem_names[png_stem_index]
                self.cleanup_png_by_stem(output_folder_path, png_stem_name)

        if options.generate_pdf_structures:
            self.generate_pdf_structure(output_folder_path)

        if options.generate_pdf_structures:
            print("Generating search indicies")
            self.generate_pdf_search(output_folder_path)

        if options.generate_structure:
            self.generate_structure(options)

        if options.generate_meta_from_isbn:
            print("Researching ISBN related data")
            self.generate_meta_from_isbn(options, output_folder_path)

        if options.generate_meta_from_text:
            print("Researching content data")
            self.generate_meta_from_text(options, output_folder_path)

        if options.cleanup_txts:
            txt_stem_names = self.find_txt_stem_names(output_folder_path)
            for txt_stem_index in range(len(txt_stem_names)):
                human_page_name = "".join(["page ", str(txt_stem_index + 1)])
                print("".join(["Cleaning up text for ", human_page_name]))
                txt_stem_name = txt_stem_names[txt_stem_index]
                self.cleanup_txt_by_stem(output_folder_path, txt_stem_name)

    def generate_meta_from_text(self, options, output_folder_path):
        meta_file_name = "meta.json"
        meta_file_path = os.path.join(output_folder_path, meta_file_name)
        meta_file_exists = os.path.exists(meta_file_path)

        attempt_meta_file_generation = True
        if meta_file_exists and not options.preserve_existing_meta:
            attempt_meta_file_generation = False

        if not attempt_meta_file_generation:
            return

    def generate_meta_from_isbn(self, options, output_folder_path):
        meta_file_name = "meta.json"
        meta_file_path = os.path.join(output_folder_path, meta_file_name)
        meta_file_exists = os.path.exists(meta_file_path)

        attempt_meta_file_generation = True
        if meta_file_exists and options.preserve_existing_meta:
            attempt_meta_file_generation = False

        if not attempt_meta_file_generation:
            return

        potential_isbns = self.find_isbns(output_folder_path)
        if len(potential_isbns) > 0:
            for potential_isbn in potential_isbns:
                meta = self.lookup_meta_by_isbn(potential_isbn)
                if meta is None:
                    continue
                with open(meta_file_path, "w") as meta_file:
                    meta_file.write("{\n")

                    meta_file.write('  "isbn" : "')
                    meta_file.write(meta.isbn)
                    meta_file.write('",\n')

                    meta_file.write('  "title" : "')
                    meta_file.write(meta.title)
                    meta_file.write('",\n')

                    meta_file.write('  "authors" : [\n')
                    is_first_author = True
                    for author in meta.authors:
                        if is_first_author:
                            is_first_author = False
                        else:
                            meta_file.write(",\n")
                        meta_file.write('    "')
                        meta_file.write(author)
                        meta_file.write('"\n')

                    meta_file.write("  ],\n")

                    meta_file.write('  "thumbnail_url" : "')
                    meta_file.write(meta.thumbnail_url)
                    meta_file.write('"\n')

                    meta_file.write("}\n")
                break

    def generate_structure(self, options):
        directory_names = list[str]()
        for directory_path, _, _ in os.walk(options.output_root_path):
            directory_name_split = os.path.split(directory_path)
            parent_directory_name = directory_name_split[0]
            if len(parent_directory_name) == 0:
                continue
            directory_name = directory_name_split[1]
            directory_names.append(directory_name)

        structure_file_name = "structure.json"
        structure_file_path = os.path.join(
            options.output_root_path, structure_file_name
        )
        with open(structure_file_path, "w") as structure_file:
            structure_file.write("{\n")

            structure_file.write('  "publications" : [\n')
            is_first_directory = True
            for directory_name in directory_names:
                if is_first_directory:
                    is_first_directory = False
                else:
                    structure_file.write(",\n")
                structure_file.write('    { "folder" : "')
                structure_file.write(directory_name)
                structure_file.write('"')

                structure_file.write(" }")
            structure_file.write("\n  ]\n")
            structure_file.write("}\n")

    def generate_pdf_structure(self, output_folder_path):
        structure_file_name = "structure.json"
        structure_file_path = os.path.join(output_folder_path, structure_file_name)
        with open(structure_file_path, "w") as sturcture_file:
            sturcture_file.write("{\n")

            sturcture_file.write('  "pages" : [\n')
            is_first_directory = True
            for txt_stem_name in self.find_txt_stem_names(output_folder_path):
                jpg_file_name = "".join([txt_stem_name, ".jpg"])

                if is_first_directory:
                    is_first_directory = False
                else:
                    sturcture_file.write(",\n")
                sturcture_file.write('    { "file" : "')
                sturcture_file.write(jpg_file_name)
                sturcture_file.write('"')

                sturcture_file.write(" }")
            sturcture_file.write("\n  ]\n")

            sturcture_file.write("}\n")

    def generate_pdf_search(self, output_folder_path):
        count_by_word_by_page_stem_name = self.calculate_word_frequencies_by_page(
            output_folder_path
        )
        count_by_word = dict[str, dict[str, int]]()
        for page_stem_name in count_by_word_by_page_stem_name.keys():
            page_specific_count_by_word = count_by_word_by_page_stem_name[
                page_stem_name
            ]
            for word in page_specific_count_by_word.keys():
                count = page_specific_count_by_word[word]
                existing_count = 0
                if word in count_by_word:
                    existing_count = count_by_word[word]
                count += existing_count
                count_by_word[word] = count

        search_file_name = "search.json"
        search_file_path = os.path.join(output_folder_path, search_file_name)
        with open(search_file_path, "w") as search_file:
            search_file.write("{\n")

            search_file.write('  "word_frequencies" : [\n')
            is_first_word_frequency = True
            for word in count_by_word:
                count = count_by_word[word]
                if is_first_word_frequency:
                    is_first_word_frequency = False
                else:
                    search_file.write(",\n")
                search_file.write('    { "')
                search_file.write(word)
                search_file.write('" : ')
                search_file.write(str(count))
                search_file.write(" }")
            search_file.write("\n  ]\n")

            search_file.write("}\n")

    def calculate_word_frequencies_by_page(self, output_folder_path):
        page_txt_stem_names = self.find_txt_stem_names(output_folder_path)
        count_by_word_by_page_stem_name = dict[str, dict[str, int]]()
        for page_txt_stem_name in page_txt_stem_names:
            page_txt_file_name = "".join([page_txt_stem_name, ".txt"])
            page_txt_file_path = os.path.join(output_folder_path, page_txt_file_name)
            with open(page_txt_file_path, "r") as page_txt_file:
                page_txt_contents = page_txt_file.read()
            words = page_txt_contents.split()
            count_by_word = dict[str, int]()
            for word in words:
                lower_word = word.lower()
                safe_word_characters = list[str]()
                for character in lower_word:
                    if character in "abcdefghijklmnopqrstuvwxyz1234567890.,@$":
                        safe_word_characters.append(character)
                safe_word = "".join(safe_word_characters)
                if len(safe_word) > 0:
                    count = 0
                    if safe_word in count_by_word:
                        count = count_by_word[safe_word]
                    count += 1
                    count_by_word[safe_word] = count
            count_by_word_by_page_stem_name[page_txt_stem_name] = count_by_word
        return count_by_word_by_page_stem_name

    def cleanup_png_by_stem(self, output_folder_path: str, png_stem_name: str):
        png_file_name = "".join([png_stem_name, ".png"])

        png_file_path = os.path.join(output_folder_path, png_file_name)
        delete_png_command = ["rm", png_file_path]
        runner = Runner()
        delete_png_result = runner.execute(delete_png_command)
        if len(delete_png_result.error_text) > 0:
            print(delete_png_result.error_text)
            exit()

    def generate_jpg_file(
        self, output_folder_path: str, page_stem_name: str, input_png_path: str
    ) -> None:
        output_jpg_name = "".join([page_stem_name, ".jpg"])
        output_jpg_path = os.path.join(output_folder_path, output_jpg_name)
        to_jpg_command = [
            "convert",
            input_png_path,
            "-strip",
            "-interlace",
            "Plane",
            "-quality",
            "85%",
            output_jpg_path,
        ]
        runner = Runner()
        to_jpg_result = runner.execute(to_jpg_command)
        if len(to_jpg_result.error_text) > 0:
            print(to_jpg_result.error_text)
            exit()
    
    def generate_bordered_png_file(
        self, output_folder_path: str, page_stem_name: str, input_png_path: str
    ) -> None:
        output_bordered_name = "".join([page_stem_name, ".bordered.png"])
        output_bordered_path = os.path.join(output_folder_path, output_bordered_name)
        to_bordered_command = [
            "convert",
            input_png_path,
            "-bordercolor",
            "White",
            "-border",
            "10x10",
            output_bordered_path,
        ]
        runner = Runner()
        to_bordered_result = runner.execute(to_bordered_command)
        if len(to_bordered_result.error_text) > 0:
            print(to_bordered_result.error_text)
            exit()


    def extract_txt_file(self, input_png_path: str, output_txt_path: str) -> None:
        to_txt_command = ["tesseract", input_png_path, output_txt_path]
        runner = Runner()
        to_txt_result = runner.execute(to_txt_command)
        if len(
            to_txt_result.error_text
        ) > 0 and not to_txt_result.error_text.startswith("Detected"):
            print(to_txt_result.error_text)
            exit()

    def generate_png_files(self, pdf_file_path: str, output_folder_path: str) -> None:
        page_file_prefix = "page"
        output_png_prefix_path = os.path.join(output_folder_path, page_file_prefix)
        to_png_command = ["pdftoppm", "-r", "300", "-png", pdf_file_path, output_png_prefix_path]
        runner = Runner()
        to_png_result = runner.execute(to_png_command)
        if len(to_png_result.error_text) > 0:
            print(to_png_result.error_text)
            exit()

    def find_png_stem_names(self, output_folder_path: str) -> list[str]:
        png_stem_names = list[str]()
        for root, dirs, file_names in os.walk(output_folder_path):
            for file_name in file_names:
                if file_name.endswith(".png"):
                    stem_name = Path(file_name).stem
                    png_stem_names.append(stem_name)
        png_stem_names.sort()
        return png_stem_names

    def find_txt_stem_names(self, output_folder_path: str) -> list[str]:
        txt_stem_names = list[str]()
        for root, dirs, file_names in os.walk(output_folder_path):
            for file_name in file_names:
                if file_name.endswith(".txt"):
                    stem_name = Path(file_name).stem
                    txt_stem_names.append(stem_name)
        txt_stem_names.sort()
        return txt_stem_names

    def cleanup_txt_by_stem(self, output_folder_path: str, txt_stem_name: str):
        txt_file_name = "".join([txt_stem_name, ".txt"])
        txt_file_path = os.path.join(output_folder_path, txt_file_name)
        delete_txt_command = ["rm", txt_file_path]
        runner = Runner()
        delete_txt_result = runner.execute(delete_txt_command)
        if len(delete_txt_result.error_text) > 0:
            print(delete_txt_result.error_text)
            exit()

        bordered_file_name = "".join([txt_stem_name, ".bordered.png"])
        bordered_file_path = os.path.join(output_folder_path, bordered_file_name)
        delete_bordered_command = ["rm", bordered_file_path]
        runner = Runner()
        delete_bordered_result = runner.execute(delete_bordered_command)
        if len(delete_bordered_result.error_text) > 0:
            print(delete_bordered_result.error_text)
            exit()


    def find_isbns(self, output_folder_path) -> list[str]:
        page_txt_stem_names = self.find_txt_stem_names(output_folder_path)

        # exclude unlikely pages in the middle of the publication
        start_range_count = 10
        end_range_count = 5

        while len(page_txt_stem_names) > (start_range_count + end_range_count):
            del page_txt_stem_names[start_range_count]

        isbn_prefixes = list[str](
            [
                "ISBN-13",
                "ISBN-10",
                "ISBN",
                "International Standard Book Number-13",
                "International Standard Book Number-10",
                "International Standard Book Number",
            ]
        )

        isbns = list[str]()

        for page_txt_stem_name in page_txt_stem_names:
            page_txt_file_name = "".join([page_txt_stem_name, ".txt"])
            page_txt_file_path = os.path.join(output_folder_path, page_txt_file_name)
            with open(page_txt_file_path, "r") as page_txt_file:
                page_txt_lines = page_txt_file.readlines()

            for line in page_txt_lines:
                prefix_found = False
                prefix_end_index = 0
                for prefix in isbn_prefixes:
                    if prefix not in line:
                        continue
                    prefix_start_index = line.index(prefix)
                    prefix_found = True
                    prefix_end_index = prefix_start_index + len(prefix) - 1
                    break

                if not prefix_found:
                    continue

                valid_digits = "01234567890"
                valid_characters = " :-" + valid_digits

                number_characters = list[str]()
                character_index = prefix_end_index + 2
                while len(number_characters) < 13:
                    character = line[character_index]
                    if not character in valid_characters:
                        break
                    if character in valid_digits:
                        number_characters.append(character)
                    character_index += 1
                if len(number_characters) in range(10, 13 + 1):
                    isbn = "".join(number_characters)
                    isbns.append(isbn)
        return isbns

    def lookup_meta_by_isbn(self, potential_isbn: str) -> Meta:
        url = "https://www.googleapis.com/books/v1/volumes?q=isbn:" + potential_isbn
        lookup_response_data = urllib.request.urlopen(url).read()
        lookup_response_text = lookup_response_data.decode("utf-8")
        lookup_response = json.loads(lookup_response_text)

        isbn: str = None

        found_match = lookup_response["totalItems"] > 0
        if found_match:
            isbn = potential_isbn

        if (not found_match) and len(potential_isbn) > 10:
            potential_short_isbn = potential_isbn[:10]
            url = (
                "https://www.googleapis.com/books/v1/volumes?q=isbn:"
                + potential_short_isbn
            )
            lookup_response_data = urllib.request.urlopen(url).read()
            lookup_response_text = lookup_response_data.decode("utf-8")
            lookup_response = json.loads(lookup_response_text)
            found_match = lookup_response["totalItems"] > 0
            if found_match:
                isbn = potential_short_isbn

        if not found_match:
            return None

        first_item = lookup_response["items"][0]
        volume_info = first_item["volumeInfo"]
        meta = Meta()
        meta.isbn = isbn
        meta.authors = volume_info["authors"]
        meta.title = volume_info["title"]
        meta.thumbnail_url = volume_info["imageLinks"]["thumbnail"]
        return meta


if __name__ == "__main__":
    
    input_folder = ''
    output_folder = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hi:o:",["input=","output="])
    except getopt.GetoptError:
        print ('test.py -i <inputfolder> -o <outputfolder>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('generate.py -i <inputfolder> -o <outputfolder>')
            sys.exit()
        elif opt in ("-i", "--input"):
            input_folder = arg
        elif opt in ("-o", "--output"):
            output_folder = arg
    print ('Reading from ' + input_folder)
    print ('Generating to ' + output_folder)

    options = Options()
    options.input_root_path = input_folder
    options.output_root_path = output_folder

    pdf_stem_names = list[str]()
    for root, dirs, file_names in os.walk(options.input_root_path):
        for file_name in file_names:
            if file_name.endswith(".pdf"):
                stem_name = Path(file_name).stem
                pdf_stem_names.append(stem_name)

    for pdf_stem_name in pdf_stem_names:
        pdf_file_name = "".join([pdf_stem_name, ".pdf"])
        input_path = os.path.join(options.input_root_path, pdf_file_name)
        output_path = os.path.join(options.output_root_path, pdf_stem_name)

        process_pdf = True
        output_path_exists = os.path.exists(output_path)
        if output_path_exists and options.ignore_existing_directories:
            process_pdf = False

        if process_pdf:
            print("".join(["Extracting pages from ", pdf_file_name]))
            if not output_path_exists:
                os.makedirs(output_path)
            extractor = Extractor()
            extractor.extract(options, input_path, output_path)
        else:
            print("".join(["Ignoring ", pdf_file_name]))
