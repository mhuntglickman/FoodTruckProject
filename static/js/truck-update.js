"use strict";
function blankOut(divName, truck_names, truck_ids)
{
  // Wipe the div clean before inserting new information 5/28/2016
  // 
  document.getElementById(divName).innerHTML = "";
  document.getElementById(divName).style.font = "26px Rancho";
  for (i = 0; i < cars.length; i++) { 
    text += cars[i] + "<br>";
  }
  document.getElementById(divName).innerHTML += '';

}



// send the event to function for evaluation
function submitTrucks(evt) {
    //stop the default event
    evt.preventDefault();

	

    var truck_array = $("#update-truck-form").serialize();
    console.log(truck_array);

    $.post("/update-trucks", truck_array, function (results)
           {
           	  
              console.log(results)
              truck_watcher = results['trucks'].get('name')
              truck_watcher_id = results['trucks'].get('truck_id')

   
              // no_watcher = my_dict['other_trucks'].get('name')
              // no_watcher_id = my_dict['other_trucks'].get('truck_id')
    

              // //clean out the div for repopulation and send along the lists
              // blankOut('watching', truck_watcher,truck_watcher_id )
              // blankOut('not-watching', no_watcher, no_watcher_id)

              console.log("ready to repopulate")

              debugger;



           });
}

$("#btn-ser1").click(submitTrucks);
