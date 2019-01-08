# xetrapal (क्षेत्रपाल)
हिन्दी एवं अन्य भारतीय भाशाओं में इंटरनेट से सामग्री को साझा करने एवं स्वतंत्र रूप से विश्लेषण करने के उपकरण

Orchestration and automation framework for web based task work, data analysis and mining, particularly in Indic languages

## Components

### Jeeva

Controls the basic functions - setup, read config, set up logging and error handling.

### Astra

Objects that are usually from interfaces to other services. For example, a Selenium browser handle is an astra, as is a telegram chat bot controller object.
An astra is defined in a <name>astras.py file. An astra file will generally contain a class definition of a wrapper object (or an import of a wrapper library)
followed by a get_ function, that takes the configuration from the Xetrapal's config file and uses it to set up the astra. The get_ function returns a handle to the astra object.


### Karma

Functions carried out by the Jeeva using an Astra. Can be simple functions or complex workflows.

Contact Suryaveer Gaur (gaursurya33 at gmail dot com)
