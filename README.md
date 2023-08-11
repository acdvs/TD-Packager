# TD-Packager

A packaged TouchDesigner component that simplifies the process of properly packaging a .tox file for external use. (Yes, this component is used to package itself!)

## Basic Usage

1. Download the .tox file from the `/dist` folder and place it in a location convenient for your project.
2. Drag and drop it into your project.
3. Set the Target COMP in the Settings parameters tab to the COMP you want to package.
4. Click the Package button.

## Features

- By providing a Custom Name, you can change the base file name to something other than the name of your Target COMP.
- Versioned naming is enabled by default. Turn this off if you don't want a version suffix in the file name.
- The final computed path and file name are dynamically updated so you can easily tell what the end result will be before you package your component.
- External files linked on child ops are unlinked to containerize the package and relinked after building. This can be turned off.
- Certain custom parameters are reset to their default values and restored after building to clear out development and testing values. This can be turned off.  
  Affected parameter types:
  - Non-read-only
  - Read-only constant
  - Read-only Python
- You can define `PreBuild` and `PostBuild` hooks in the Target COMP module that will be called just before and after the .tox file is saved. These methods take no arguments and the extension must be promoted.   
  The full life cycle is:
  1. `PreBuild`
  2. Files unlinked, parameters cleared (if enabled)
  3. .tox saved
  4. Files relinked, parameters restored (if enabled)
  5. `PostBuild`

## Contributing

Simply make changes in the project file, increase the Version parameter (following [semver](https://semver.org)), and click the Package button.