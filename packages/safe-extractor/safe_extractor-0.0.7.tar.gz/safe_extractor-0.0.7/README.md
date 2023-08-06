# safe_extractor
Some code that supposedly extracts zip/tar archives safely.

No guarantees.

## Install
`pip install safe_extractor`

## Usage
```
  from safe_extractor import safe_extractor
  safe_extractor.untar_it("myfile.tar.gz", extract_path='.')
  safe_extractor.unzip_it("myfile.zip", extract_path='.')
```
