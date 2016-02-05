/**
 * Created by pradyumnad on 2/4/16.
 */

/**
 //    Go to the index page of the websites ausopen.com or usopen.org
 //      Open console, and run the below code
 **/

var source = new Array();

var tags = $("a.white");

$.each(tags, function (index, val) {
    source.push(this.getAttribute('href'))
});

print(source);