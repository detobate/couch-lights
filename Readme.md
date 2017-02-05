Couch-Lights
============

Alexa controlled LED strip lights, using a [Particle Photon](https://store.particle.io/#photon) and [Particle.io](https://particle.io)

Particle.IO
-----------
Register your Particle Photon with [Particle.IO](https://particle.io) and upload [couch-lights.ino](https://github.com/detobate/couch-lights/blob/master/couch-lights.ino)
Copy your device ID and access token, you'll need to configure the AWS Lambda with them.

Alexa Skill
-----------
Register at [https://developer.amazon.com](https://developer.amazon.com) and create a new Alexa Skill.
Use [couch-lights-alexa-skill-intent.json](https://github.com/detobate/couch-lights/blob/master/couch-lights-alexa-skill-intent.json) for the Intent Schema.
Create a custom slot type called "COLOUR" and give it some basic colour examples.  You don't have add every single colour, Alexa just uses these as examples.

**Sample Utterances:**

    turnOff turn off
    turnOff off
    turnOn turn on
    turnOn on
    setColour set color {colour}
    setColour set colour {colour}


AWS Lambda
----------
Create a lambda using [couch-lights-lambda.py](https://github.com/detobate/couch-lights/blob/master/couch-lights-lambda.py)

The Particle.IO device ID and access token need to be created as environment variables in the lambda.
