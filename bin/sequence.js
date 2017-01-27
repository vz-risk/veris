function errorHandler(e) {
  var msg = '';

  switch (e.code) {
    case FileError.QUOTA_EXCEEDED_ERR:
      msg = 'QUOTA_EXCEEDED_ERR';
      break;
    case FileError.NOT_FOUND_ERR:
      msg = 'NOT_FOUND_ERR';
      break;
    case FileError.SECURITY_ERR:
      msg = 'SECURITY_ERR';
      break;
    case FileError.INVALID_MODIFICATION_ERR:
      msg = 'INVALID_MODIFICATION_ERR';
      break;
    case FileError.INVALID_STATE_ERR:
      msg = 'INVALID_STATE_ERR';
      break;
    default:
      msg = 'Unknown Error';
      break;
  };

  console.log('Error: ' + msg);
}

function recurseJSON( obj, prefix="", properties = [] ) {
    //console.log(obj);
    //console.log(prefix);
    for (prop in obj) {
        if (obj[prop].constructor.name == "Number") {
            //console.log("chose number");
            properties.push(prefix + prop + "." + obj[prop]);
            //console.log("adding " + prefix + prop + "." + obj[prop]);
        } else if (obj[prop].constructor.name == "String") {
            //console.log("chose string.");
            properties.push(prefix + prop + "." + obj[prop]);
            //console.log("adding " + prefix + prop + "." + obj[prop]);
        } else if (obj[prop].constructor.name == "Array") {
            //console.log("chose array");
            new_properties = recurseJSON(obj[prop], prefix + prop + ".", properties);
            //console.log(properties);
            //console.log(new_properties);
            //properties = properties.concat(new_properties);
            properties = new_properties;
        } else if (obj[prop].constructor.name == "Object") {
            //console.log("chose object");
            new_properties = recurseJSON(obj[prop], prefix + prop + ".", properties);
            //console.log(properties);
            //console.log(new_properties);
            //properties = properties.concat(new_properties);
            properties = new_properties;
        } else {
            console.log("Property type: " + obj[prop].constructor.name + " not found.");
        };
    };
    return properties;
}

function add_table_row(features, size) {
    console.log("starting add_table_row");
    console.log("features length:" + features.length);
    size++;
    var row = "<tr id='seqTableRow" + size + "'>\n";
    for (var i = 0; i < features.length; i++) {
        row = row + "<td><input type='radio' id='" + size + "," + i + "'></td>\n";
    }
    row = row + "</tr>\n";
    return row;
}

$(document).ready(function() {
    var counter = 1;

    function updateList() {
        // TODO: Remove everything from Div
        for (prop in inJSON) {
            if (inJSON.hasOwnProperty(prop))  {
                $("<option value="+prop+">"+prop+"</option>").appendTo("#filesDivSelect");
            }
        }
    }

    console.log("Document Ready");

    var inJSON = {};
    var outJSON = {};

    // https://developer.mozilla.org/en-US/docs/Web/API/Blob
    $('#inDir').change(function() {
        for (var i = 0; i < this.files.length; i++) {
            if ((this.files[i].name.substr(-4) == "json") & 
                !(outJSON.hasOwnProperty(this.files[i].name))) {
                    console.log("adding " + this.files[i].name);
                    var reader = new FileReader();

                    reader.readAsText(this.files[i]);
                    // https://developer.mozilla.org/en-US/docs/Web/API/FileReader
                    // while (reader.readyState != 2) {
                    //     // http://stackoverflow.com/questions/951021/what-is-the-javascript-version-of-sleep
                        setTimeout(function() {
                            console.log('wait over!!');
                        }, 500);
                    // };
                    // await (reader.readyState == 2);
                    inJSON[this.files[i].name] = $.getJSON(reader.result);
                    console.log(inJSON);
            };
        };
        console.log(Object.keys(inJSON).length);
        console.log(inJSON);
        updateList();
    });

    $('#outDir').change(function() {
        var reader = new FileReader();

        for (var i = 0; i < this.files.length; i++) {
            if ((this.files[i].name.substr(-4) == "json") & 
                !(inJSON.hasOwnProperty(this.files[i].name))) {
                    console.log("removing " + this.files[i].name);
                    delete inJSON[this.files[i].name];

                    updateList();
            };
        };
        console.log(Object.keys(inJSON).length);
    });

    $('#filesDivSelect').change(function() {
        console.log("New file selected.");
        prop = $( "#filesDivSelect" ).val();
        obj = inJSON[prop];
        // Read the object, fine the features under the sequenced features
        features = recurseJSON(obj);
        $('#seqTable').data('features', features);
        // Create the header
        var table_header = "<tr>";
        for (feature in features) {
            table_header = table_header + "<th>" + features[feature] + "</th>"
        };
        table_header = table_header + "</tr>";
        $('#seqTable').append(table_header);
        // TODO: Create the first line and code to add lines
        $('#seqTable').append(add_table_row(features, 0));
    });

    $('#addButton').live('click', function() {
        console.log("Adding row.");
        var row = add_table_row(
            $('#seqTable').data('features'),
            $('#seqTable').length - 1
        );
        $('#seqTable').append(row);
    });

    $('#delButton').live('click', function() {
        console.log("Removing row.");
        var last_row = $('#seqTable').length - 1;
        $('#seqTable').remove('#seqTableRow' + last_row);  
    })

    // $('#loadButton').live('click', function() {
    //     console.log('load button clicked.');

    //     fs.root.getDirectory($('#inDir').text(), {create: false}, function(dirEntry){
    //       var dirReader = dirEntry.createReader();
    //       dirReader.readEntries(function(entries) {
    //         for(var i = 0; i < entries.length; i++) {
    //           var entry = entries[i];
    //           if (entry.isDirectory){
    //             console.log('Directory: ' + entry.fullPath);
    //           }
    //           else if (entry.isFile){
    //             console.log('File: ' + entry.fullPath);
    //           }
    //         }

    //       }, errorHandler);
    //     }, errorHandler);

    //     fs.root.getDirectory($('#outDir').text(), {}, function(dirEntry){
    //       var dirReader = dirEntry.createReader();
    //       dirReader.readEntries(function(entries) {
    //         for(var i = 0; i < entries.length; i++) {
    //           var entry = entries[i];
    //           if (entry.isDirectory){
    //             console.log('Directory: ' + entry.fullPath);
    //           }
    //           else if (entry.isFile){
    //             console.log('File: ' + entry.fullPath);
    //           }
    //         }

    //       }, errorHandler);
    //     }, errorHandler);
    // });

    // $('#addButton').live('click', function() {
    //     $('<p><input class="textbox1" type="text" id="sign_symptom_name_' + counter + '" size="22" name="sign_symptom_name_' + counter + '" value="" placeholder="Sign or Symptom Name" /> <input class="textbox2" type="text" id="sign_symptom_value_' + counter + '" size="20" name="sign_symptom_value_' + counter + '" value="" placeholder="Sign or Symptom Value" /> <a href="#" id="rmSignSymptom">Remove</a></p>').appendTo("#inDiv");
    //     counter++;
    //     return false
    //  });


    // $('#rmRow').live('click', function() {
    //     if( counter > 1 ) {
    //             $(this).parent('p').remove();
    //             counter--;
    //     }
    //     return false;
    // });
});
