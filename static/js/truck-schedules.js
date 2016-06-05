"use strict";

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
  infoWindow.setPosition(pos);
  infoWindow.setContent(browserHasGeolocation ?
                        'Error: The Geolocation service failed.' :
                        'Error: Your browser doesn\'t support geolocation.');
}

//////////////////////////////////////////////////////////////////
// latt, longi are the destination coordinates
// pos are the origin geo location lat long coordinates

function calculateAndDisplayRoute(directionsService, directionsDisplay, origin_latt, origin_lng, latt, longi ){

    directionsService.route({
            origin: new google.maps.LatLng(37.788633399999995, -122.4114752), // Pass this in place of the address 'Akin Ogunlewe street VI'
            //origin: new google.maps.LatLng(origin_latt, origin_lng), // Pass this in place of the address 'Akin Ogunlewe street VI'
            destination: new google.maps.LatLng(latt, longi), // Pass this in place of the address 'Falolu road Surulere'
            travelMode: google.maps.TravelMode.DRIVING
        }, function(response, status){

            if (status === google.maps.DirectionsStatus.OK){
                directionsDisplay.setDirections(response);
            } 
            else{
                window.alert('Directions request failed due to ' + status);
            }
    
    });

}


function initMyMap(latt, longi, start_time, end_time, truck_name){
    var directionsService = new google.maps.DirectionsService;
    var directionsDisplay = new google.maps.DirectionsRenderer; 
    $( document ).ready(function() {
        console.log( "document loaded" );
    });
    

    //Try W3C Geolocation (Preferred)
    function initialize() {
      var myOptions = {
        zoom: 6,
        mapTypeId: google.maps.MapTypeId.ROADMAP
      };


      var map = new google.maps.Map(document.getElementById("map"), myOptions);

      // Try W3C Geolocation (Preferred)
      if(navigator.geolocation) {
        browserSupportFlag = true;
        navigator.geolocation.getCurrentPosition(function(position) {
          initialLocation = new google.maps.LatLng(position.coords.latitude,position.coords.longitude);
          map.setCenter(initialLocation);
        }, function() {
          handleNoGeolocation(browserSupportFlag);
        });
      }
      // Browser doesn't support Geolocation
      else {
        browserSupportFlag = false;
        handleNoGeolocation(browserSupportFlag);
      }

      function handleNoGeolocation(errorFlag) {
        if (errorFlag == true) {
          alert("Geolocation service failed.");
          initialLocation = sanfrancisco;
        } 
        map.setCenter(initialLocation);
      }
    }

    //Create the map and set the pin based on lat and lng sent in from DB
    var map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: latt, lng: longi},
        zoom: 14,
        mapTypeControl: true,
        zoomControl: true,
        scaleControl: true,
        streetViewControl: true,
        rotateControl: true

    
    });
    //Drop a marker for the truck
    var marker = new google.maps.Marker({
        position: {lat: latt, lng: longi},
        map: map,
        title: truck_name + '\nHours: ' + start_time + " - "+ end_time,
        icon: 'http://imageshack.com/a/img924/7348/BZGR4q.png'
        
        });

    var infoWindow = new google.maps.InfoWindow({map: map});
    
    
    debugger;
    
    
    // debugger;
    // console.log(position.coords.latitude)
    //setTimeout(function(){ alert("Hello"); }, 3000);
    
    $( document ).ready(function() {
        directionsDisplay.setMap(map); 
    });
    $( document ).ready(function() {
        calculateAndDisplayRoute(directionsService, directionsDisplay, latt, longi);
    });
  
}






// send the event to function for evaluation
function submitSchedule(evt) {
    //stop the default event
    evt.preventDefault();

    var formInputs = {
        "day": $("#day").val(),
        "truck_id": $("#truck-id").val()
    };
    
    
    $.get("/truck_schedule", 
    	   formInputs, function (myScheduleDict)
           {
            //Immediately check to see if the object is empty
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
                
                    initMyMap(myScheduleDict.lattitude, myScheduleDict.longitude, myScheduleDict.start_time, myScheduleDict.end_time, myScheduleDict.truck_name);
                }
           });
}// End of anonymous success function from AJAX call


//////////////////////////////////////////////////////////////////////////////
// Click event button for truck.html
// 
$("#display-schedule").on("submit", submitSchedule);




