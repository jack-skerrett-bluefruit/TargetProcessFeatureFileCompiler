# Turn your target process tests into Gherkin Feature Files

Use this script with all it's wonderful capabilities to turn your boring old Target Process test cases into all singing all dancing Feature Files!

# So how does it work?

* Firstly, make sure you have Python 3 installed (you shouldn't need to worry about a virtual environment or installing any modules)
* Then, you can simply call "feature_file_compiler.py --help" from your command line and away you go!

## Arguments

Let me explain what all the arguments mean in a bit more detail

### Entity

* This is a list of Target Process entities that you wish to turn into a Feature File. You can pass in a list of Projects, Features, Test Plans or Test Cases, like so:  "feature_file_compiler 27623 38575 38598"