# mars-webapp

`mars-webapp` is a blog webapp based on Flask.
 [http://www.kevenwu.com](http://www.kevenwu.com)

## ScreenShot
![screen1](http://7xr7bq.com1.z0.glb.clouddn.com/mars_webapp_screen1.png)

![screen2](http://7xr7bq.com1.z0.glb.clouddn.com/mars_webapp_screen2.png)

## Usage
### Install Dependences
    pip install -r requirements.txt

### Initialize Database
    python shell.py 
    >>>from app import db
    >>>db.create_all()
    >>>exit()

### Run
    python run.py

## Contributing
Please fork repository and contribute using pull requests.

## Credits
kevenwu

## License

    Copyright 2015 Kevenwu

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    
    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
