Made with Arc v.10.2

Setup is easy:

-Unzip this folder
-Open an instance of ArcMap
-Right click in the ArcToolbox window
-Click "Add Toolbox"
-Navigate to this folder and click on the toolbox included (Reflectance.tbx)
-Double click on the tool you need


Some important notes: 

Update 07/14/2014. calcReflectance method updated to show convert solar zenith to radians (was giving
wierd values with degrees.

There are two script tools included one for using the metadata from a Landsat download and one for a custom
reflectance calculation using your own metadata.

The majority of the questions you have can probably be answered in the script comments. Don't be alarmed by 
lots of negative values; to avoid oversaturation the satellites "shoot dark" (not the technical term). Read 
the Landsat documentation for more detail, but basically what you see is what you get, and you get lots of negatives.

I make no claims as to the scientific integrity of these tools; this was a side project born after a few days of 
reading the Landsat 7 handbook. Specifically tailored for a certain project; at the very least this can serve as a 
starting point for your own stuff.

Always consult the Landsat documentation first (they are announcing the release of a new version of the documentation 
at the time this document was written [03/26/2014]).

Feel free to use any and all portions of these scripts in your own work. At your own risk, of course.

Email questions, comments, furious rants, or plesant suggestions to:

kochaver.python@gmail.com


-------------------------------------------------------------------------------------------------------------------------
Steve Kochaver 03/2014