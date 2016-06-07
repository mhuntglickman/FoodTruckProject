"use strict";



//////////////////////////////////////////////////////////////////
// 
// Then call buildHTML()to insert each new line built from
// the returned JSON response. 5/31/2016
// 
function AddBackHTML(divName, truck_names=[], truck_ids=[])
{
  
  //document.getElementById(divName).innerHTML +="<ul>";

  var newhtml = "";

  newhtml += "<ul>";
  ////////////////////////////////////////////////////////////////////
  // iterate over the list of items to build and use the buildHTML() to 
  // insert each one into the div
  
  for (var i = 0; i < truck_ids.length; i++) {


    //build a string to with the result lists
    newhtml += "<li class=\"user-item-list\"><span><a href=\"/trucks/" + truck_ids[i] + "\"> " + truck_names[i] + "  </a>";
    //var Add_In = "<span><a href=\"/trucks/" + truck_ids[i] + ">" + truck_names[i] + "</a>";
    //document.getElementById(divName).innerHTML += Add_In;
    

    /////////////////////////////////////////////////////////
    // each new a href also requires a checkbox be created 
    //Add_In = "<input type=\"checkbox\" name=\"" + truck_ids[i] + "\"><br>";
    if (divName == 'watching'){
    newhtml += "<button type=\"button\" name="  + truck_ids[i] +  " class=\"btn btn-danger btn-xs button-space remove-truck\">Remove Me!</button></span></li>";

    //TO DO: take out before career day.  Striclty for debugging purposes.
    //console.log(Add_In);
    //debugger;

    //document.getElementById(divName).innerHTML +=Add_In;
    }
    else{

      newhtml += "<button type=\"button\" name="  + truck_ids[i] +  " class=\"btn btn-default btn-xs button-space add-truck\">Add Me!</button></span></li>";

     //TO DO: take out before career day.  Striclty for debugging purposes.
      //console.log(Add_In);
      //debugger;

      //document.getElementById(divName).innerHTML +=Add_In;
    }

  } //End of for loop
  

  newhtml += "</ul>"

  document.getElementById(divName).innerHTML = newhtml;


}

// send the event to function for evaluation
function submitTrucks(truck_id) {
    
    //stop the default 'submit' event
    //evt.preventDefault();

    // var truck_array = $("#update-truck-form").serialize();

    console.log('Do Update',truck_id )

    var tdata = {
      tid: truck_id
    }
    
    $.post("/update-trucks", tdata, function (results)
           {
           	  
              /////////////////////////////////////////
              //Wipe out the html in a div
              //
              document.getElementById("watching").innerHTML = "";
              document.getElementById("not-watching").innerHTML = "";


              ///////////////////////////////////////////////////////////////
              // create a list of truck names and id's from the json result 
              // dictionary

              // Currently followed trucks of a user
              var truck_watcher = results['trucks']['name'];
              var truck_watcher_id = results['trucks']['truck_id']; 
              // Currently not followed trucks of a user
              var no_watcher = results['other_trucks']['name'];
              var no_watcher_id = results['other_trucks']['truck_id'];
              console.log(no_watcher_id, no_watcher)
              console.log(truck_watcher_id, truck_watcher)
              // debugger;


              //////////////////////////////////////////////////////////////////
              // Repopulate the html in a particular div 
              AddBackHTML("watching", truck_watcher, truck_watcher_id );
              AddBackHTML("not-watching", no_watcher, no_watcher_id);
              

              //debugger;


           });
}// End of anonymous success function from AJAX call

function alterTrucks(event){

  console.log('Truck', event.target.name);

  submitTrucks(event.target.name);
}

///////////////////////////////////
// Click event button for user.html
// 
$("#form-1").click(function(evt){

  $(".add-truck").click(alterTrucks);
  $(".remove-truck").click(alterTrucks);

});

