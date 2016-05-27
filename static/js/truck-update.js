"use strict";

// send the event to function for evaluation
function submitTrucks(evt) {
    //stop the default event
    evt.preventDefault();

	debugger;

    var truck_array = $("#update-truck-form").serialize();
    console.log(truck_array);
    debugger;

    $.post("/update-trucks", truck_array, function ()
           {
           	console.log("made it this far")
           	debugger;
           });
}

$("#btn-ser1").click(submitTrucks);
