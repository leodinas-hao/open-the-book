# open-the-book

## preps

### install `chrome`
- check this doc [here](https://www.gregbrisebois.com/posts/chromedriver-in-wsl2/)
```sh
sudo apt-get update
sudo apt-get install -y curl unzip xvfb libxi6 libgconf-2-4
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb
# check installation
google-chrome --version
```

### install `chromedriver`
- find the driver file url to match the chrome installed
  - check the chrome driver download page [here](https://chromedriver.chromium.org/downloads) 
- download & install the driver
```sh
# download the driver file
wget https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.86/linux64/chromedriver-linux64.zip

unzip chromedriver-linux64.zip
# move the file to /usr/bin
cd chromedriver-linux64/
sudo mv chromedriver /usr/bin/chromedriver
sudo chown root:root /usr/bin/chromedriver
sudo chmod +x /usr/bin/chromedriver
```
- test the driver
```sh
chromedriver --url-base=/wd/hub
# should see: ChromeDriver was started successfully
```

## references

### selenium
- [official docs](https://www.selenium.dev/documentation/)

### epub
- https://en.wikipedia.org/wiki/EPUB
- file structure
```
--ZIP Container--
mimetype
META-INF/
  container.xml
OEBPS/
  content.opf
  toc.ncx
  book-toc.html
  style.css
  cover.html
  chapter0.html
  chapter1.html
  ...
```
