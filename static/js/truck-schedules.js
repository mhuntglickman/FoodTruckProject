"use strict";

var browserSupportFlag, initialLocation, dest, start;
var map, directionsService, directionsDisplay;


function initMyMap(latt, longi, start_time, end_time, truck_name){
    directionsService = new google.maps.DirectionsService;
    directionsDisplay = new google.maps.DirectionsRenderer; 
    //Create the map and set the pin based on lat and lng sent in from DB
        map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: latt, lng: longi},
        zoom: 14,
        mapTypeControl: true,
        zoomControl: true,
        scaleControl: true,
        streetViewControl: true,
        rotateControl: true

    
    });

    $("#get-directions").show();

    dest = {
        longi:longi,
        latt:latt
    }


    // if (end_time >"12:00:00"){
    //   end_time = end_time - "12:00:00";
    //   console.log(end_time);
    // }

    //Drop a marker for the truck
    var truckMarker = new google.maps.Marker({
        position: {lat: latt, lng: longi},
        map: map,
        title: truck_name + '\nHours: ' + start_time + " - "+ end_time,
        icon: '/static/foodTruck_MapIcon.png'
        
        });

    //Debugging  
    //console.log(navigator); 
    
}

// Geolcoation utility functions
function calculateAndDisplayRoute(directionsService, directionsDisplay, dest, start){

    directionsService.route({
            // origin: new google.maps.LatLng(37.788633399999995, -122.4114752), // Pass this in place of the address 'Akin Ogunlewe street VI'
            origin: new google.maps.LatLng(start.latt, start.longi), // Pass this in place of the address 'Akin Ogunlewe street VI'
            destination: new google.maps.LatLng(dest.latt, dest.longi), // Pass this in place of the address 'Falolu road Surulere'
            travelMode: google.maps.TravelMode.DRIVING
        }, function(response, status){

            //Debugging
            //console.log('resp', response, status);

            if (status === google.maps.DirectionsStatus.OK){
                console.log('good', directionsDisplay);
                directionsDisplay.setDirections(response);
            } 
            else{

                //Debugging
                //console.log('bad');
                window.alert('Directions request failed due to ' + status);
            }
    
    });

}

function handleNoGeolocation(errorFlag) {
    if (errorFlag == true) {
        alert("Geolocation service failed.");
        initialLocation = sanfrancisco;
    } 
    
    map.setCenter(initialLocation);
}



// send the event to function for evaluation
function submitSchedule() {

    $("#get-directions").hide();
    console.log('Submit Sched', moment().format("YYYY-MM-DD"));
    //stop the default event

    var day;

    console.log('day', $("#day").val())
    
    var formInputs = {
        "day": $("#day").val() == "" ? moment().format("YYYY-MM-DD") : $("#day").val(),
        "truck_id": $("#truck-id").val()
    };


    console.log('Form:', formInputs);

    
    
    $.get("/truck_schedule", 
    	   formInputs, function (myScheduleDict)
           {
            //Immediately check to see if the object is empty

            console.log('Have schedule', myScheduleDict);

            if(jQuery.isEmptyObject(myScheduleDict))
                {
                    // Styling for the map div when there is no map to render.  
                    // This overwrites the big blank box or other messages already in
                    // the div and done in javascript not jQuery just because it
                    // is good to know both methods 6/20/2016
                    document.getElementById('map').style.backgroundColor="#89AEB3";                    
                    document.getElementById('map').innerHTML = "";
                    document.getElementById('map').style.color="#151515"; 
                    document.getElementById('map').innerHTML += '<br>No schedule available for date selected. Please pick another date.';
                    
                }
            else{
                
                    initMyMap(
                        myScheduleDict.lattitude, 
                        myScheduleDict.longitude, 
                        myScheduleDict.start_time, 
                        myScheduleDict.end_time, 
                        myScheduleDict.truck_name
                        );
                }
           });
}// End of anonymous success function from AJAX call


function getDirections(){

    if(navigator.geolocation) {
        browserSupportFlag = true;
        navigator.geolocation.getCurrentPosition(function(position) {
          initialLocation = new google.maps.LatLng(position.coords.latitude,position.coords.longitude);
          
        console.log('IL', initialLocation.lat(), initialLocation.lng());

        start = {
            longi:initialLocation.lng(),
            latt:initialLocation.lat()
        }

        //Debuggin
        //console.log('Params:', dest, start);

        map.setCenter(initialLocation);

        calculateAndDisplayRoute(directionsService, directionsDisplay, dest, start);

        directionsDisplay.setMap(map);




        }, function() {
          handleNoGeolocation(browserSupportFlag);
        });
      }
      // Browser doesn't support Geolocation
      else {
        
        browserSupportFlag = false;
        handleNoGeolocation(browserSupportFlag);
      }




}

//////////////////////////////////////////////////////////////////////////////
// Click event button for truck.html
// 
// $("#display-schedule").on("submit", submitSchedule);

$("#schedule-search").on("click", submitSchedule);
$("#schedule-search-now").on("click", submitSchedule);

$("#get-directions").hide();
$("#get-directions").on("click", getDirections);


// $( document ).ready(function() {
//   // Handler for .ready() called.
//   submitSchedule();

// });


