Utilities for copying files from `Github/Faraday` to `Dynamo/..../packages/Faraday` or v.v. and creating a JSON file using python

Notes to self:  
1. Usage for `copy_files.py`  

    Copy `copy_files.py` to your desktop or any folder other than Github/Packages to avoid it being copied  
    edit @ `line 150` `MOTHER_MODE = <number>`  
    Modes:  
    1. Dynamic mode (like mode 2 but dynamically copies files)
       copy `.py (Faraday/src to ~extra/nodesrc)` files from Github
       including `Faraday/faradaycore` to `~extra/faradaycore`
       
    2. Static mode
       copy `.py (Faraday/src to ~extra/nodesrc)` files from Github
       including `Faraday/faradaycore` to `extra/faradaycore`
       
    3. Always static (most commonly used)
       copy all `DYFs from Packages/Farad/dyf` to `Github/Faraday/dyf`
       DON'T USE THIS MODE WITH DYNAMIC UPDATE!
       
       Use then building scripts inside dynamo then pushing to github
