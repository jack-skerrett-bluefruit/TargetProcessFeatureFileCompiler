# Turn your target process tests into Gherkin Feature Files

Use this script with all it's wonderful capabilities to turn your boring old Target Process test cases into all singing all dancing Feature Files!

# So how does it work?

* Firstly, make sure you have Python 3 installed (you shouldn't need to worry about a virtual environment or installing any modules)
* You will then need to create a file called "settings.py" in the "FeatureFileGenerator" directory. Within this file you will need to declate two variables. One is 'tp_url = "https://bluefruit.tpondemand.com/api/v1/"'. For the other, you will need to create an access token from your Target Process account, and then assign it to the variable "access_token".
* Then, you can simply call "feature_file_compiler.py --help" from your command line and away you go!

## Arguments

Let me explain what all the arguments mean in a bit more detail

### Entity 

* This is a list of Target Process entities that you wish to turn into a Feature File. You can pass in a list of Projects, Features, Test Plans or Test Cases, like so:  "python feature_file_compiler.py 27623 38575 38598". This will return 3 separate Feature Files, one for each entity listed.

### Sprint Tag (-s, --sprint_tag)

* This one is a little bit broken and I would suggest not using it. I can look into fixing it if anyone would find it useful. What this does is look for what Sprint a test/behaviour was implemented in. It does this by looking for the Sprint the Linked Assignable was completed in (as Test Cases don't have this association). Things start to go south once more than one Linked Assignable exists.

### ID Tag (-i, --id_tag)

* A rare combination here, useful and usable! This puts a tag at the beginning of your test based on the Test Case ID. If you don't like the formatting, feel free to change how it adds the tag, it can be found in FeatureFileCompiler.tag_formatter.

### User Tags (-u, --user_tags)

* Add whatever tags you want to the Feature File you are construction. This could be useful if you want to mark all the tests by a certain period in time: "python feature_file_compiler.py 27623 -u v1.1".

### Target Process Tags (-t, --target_process_tags)

* Simple enough. This adds any tags from the Target Process Test Cases to the test in the Feature File.

### Exempted Tags (-x, --exempted_tags)

* Add any tags to this argument that are on Target Process Test Cases that you don't want to appear on your Feature File output: "python feature_file_compiler.py -t -x blocked".

### Last Run (-l, --last_run)

* This will add a tag that states what the state of the last run of the Test Case was, and the date on which this occured. 