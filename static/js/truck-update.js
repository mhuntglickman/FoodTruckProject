"use strict";



//////////////////////////////////////////////////////////////////
// 
// Then call buildHTML()to insert each new line built from
// the returned JSON response. 5/31/2016
// 
function AddBackHTML(divName, truck_names=[], truck_ids=[])
{
  
  // document.getElementById(divName).innerHTML +="<ul style="list-style-type:disc">";


  ////////////////////////////////////////////////////////////////////
  // iterate over the list of items to build and use the buildHTML() to 
  // insert each one into the div
  
  for (var i = 0; i < truck_ids.length; i++) {


    //build a string to with the result lists
    var Add_In = "<a href=\"/trucks/" + truck_ids[i] + "\"> " + truck_names[i] + "  </a>";
    document.getElementById(divName).innerHTML += Add_In;
    

    /////////////////////////////////////////////////////////
    // each new a href also requires a checkbox be created 
    Add_In = "<input type=\"checkbox\" name=\"" + truck_ids[i] + "\"><br>";
    

    //TO DO: take out before career day.  Striclty for debugging purposes.
    console.log(Add_In);
    //debugger;

    document.getElementById(divName).innerHTML +=Add_In;
  
  } //End of for loop
  
  console.log(Add_In);
  document.getElementById(divName).innerHTML +="<ul>";


}

// send the event to function for evaluation
function submitTrucks(evt) {
    
    //stop the default 'submit' event
    evt.preventDefault();

    var truck_array = $("#update-truck-form").serialize();

    $.post("/update-trucks", truck_array, function (results)
           {
           	  
              /////////////////////////////////////////
              //Wipe out the html in a div
              //
              document.getElementById("watching").innerHTML = "";
              document.getElementById("not-watching").innerHTML = "";

              //////////////////////////////////////////////////////
              //One time strings to build and add to this HTML
              document.getElementById("watching").innerHTML += "<h4>Click the link to get more details about the truck.<br>To Unfollow a truck, click the checkbox.<br>When you are done submit the form.</h4><br>";
              var AddHTML = "<form id=\"update-truck-form\" action=\"/update-trucks\" method=\"post\">";
              document.getElementById("watching").innerHTML += AddHTML;

              document.getElementById("not-watching").innerHTML += "<h4>Select more trucks to follow:</h4>";
              



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
              debugger;


              //////////////////////////////////////////////////////////////////
              // Repopulate the html in a particular div 
              AddBackHTML("watching", truck_watcher, truck_watcher_id );
              AddBackHTML("not-watching", no_watcher, no_watcher_id);
              

              //////////////////////////////////////////////////////
              //One time strings to build and add to this HTML
              document.getElementById("not-watching").innerHTML += "<br>";
              document.getElementById("not-watching").innerHTML += "<br>";
              document.getElementById("not-watching").innerHTML += "<button type=\"button\" id=\"btn-ser1\">Submit Your Changes</button>";
              document.getElementById("not-watching").innerHTML += "</form>";
              //debugger;


           });
}// End of anonymous success function from AJAX call


///////////////////////////////////
// Click event button for user.html
// 
$("#btn-ser1").click(submitTrucks);

