<a name="readme-top"></a>

<br />
<div align="center">
  <h3 align="center">LibraryGen</h3>

  <p align="center">
    A static site generator for PDF Libraries
  </p>
</div>


<!-- ABOUT THE PROJECT -->
## About The Project

[![Screen Shot][product-screenshot]]

Create a (static) website for reading your PDFs that can be:
* Hosted by (almost?) any webserver
* Viewed by (almost?) any browser
* Supports automatic meta data retrieval (e.g. titles and authors)

There are a lot of existing PDF library web apps out there but they tend to assume one of the following:
* It's mostly manga
* The filenames are of a set structure
* The web server can deal with a dynamic server side site

LibraryGen doesn't make these assumptions.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

At a minimum, you're going to need to two folders:
* An input folder - with your PDFs
* An output folder - where you want the web site to be generated

(I'd recommend these being all located on the same machine at least initially)


### Prerequisites

At this stage, it's only been tested on *nix like systems such as Linux and MacOS. Support for Windows is coming soon.


There are three utilities that LibraryGen relies upon to do its work.

#### Ubuntu / Debian

Here's the terminal command to install the required dependencies:

  ```sh
  sudo apt install poppler-utils imagemagick tesseract-ocr
  ```

#### NixOS

Here are the equivalent NixOS packages for your configuration.nix:

```nix
  poppler_utils
  tesseract
  imagemagick
```

### Installation


1. Clone the repo
   ```sh
   git clone https://github.com/lzcd/librarygen.git
   ```

2. Copy the index.html file to your output folder
    ```sh
    cp index.html OUTPUTFOLDER
    ```
3. Run the generator (whith INPUTFOLDER and OUTPUT folder substitued with your own input and output folders)
   ```sh
   python3 generator.py -i INPUTFOLDER -o OUTPUTFOLDER
   ```

4. Point your webserver at the output folder

5. Profit!

Anytime you add a new PDF to the input folder, simply re-run the generate command:

   ```sh
   python3 generator.py -i INPUTFOLDER -o OUTPUTFOLDER
   ```


If you don't have a webserver handy but would like to try out the website immediately, Python has a handy little webserver built in:

   ```sh
   cd OUTPUTFOLDER
   python3 -m http.server
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- USAGE EXAMPLES -->
## Usage

The generator is fine to run any time a new PDF file is added to the input folder.

It will check if it's already generated the associated files in the output folder and skip it if need be.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

I'm happy to take suggestions on what features to tackle next.

Here are some on my personal roadmap:
- [ ] Add more ways to extract / guess meta details (e.g. title)
- [ ] Increase the pretty. Decrease the ugly.
- [ ] Add Search
- [ ] Add Windows Support? 
- [ ] Add Zoom

See the [open issues](https://github.com/lzcd/librarygen/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Luke Drumm - [@lzcd](https://twitter.com/lzcd) - lzcd@hotmail.com

Project Link: [https://github.com/lzcd/librarygen](https://github.com/lzcd/librarygen)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- FAQ -->
## FAQ

### What framework(s) did you use?

None.

It's vanilla Python for the generator and vanilla JS for the web site.

Simplicity is the name of the game.

### Its sooooo slow at generating

Yep.

More than happy to receive alternate suggestions on more efficient and / or faster alternatives to the current methods of image generation and OCR.

### What's the deal with all the file manipulation?

Tesseract requires a decent resolution to do OCR (300+ dpi) and has a bug when dealing with random resolutions that requires a border to work.



<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[product-screenshot]: images/screenshot.jpg
