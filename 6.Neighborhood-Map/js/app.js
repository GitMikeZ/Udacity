/*
* @description A varaible in the global namespace called 'map'.
* @type {object}
*/
var map;

/*
* @description A varaible in the global namespace called 'infoWindow'.
* @type {object}
*/
var infoWindow;

/*
* @description A varaible in the global namespace called 'Attractions'.
* @type {Array}
*/
var Attractions = [
   {
        name: 'Big Ben',
        lat: 51.5007,
        lng: -0.1246,
   },
   {
        name: 'British Museum',
        lat: 51.5194,
        lng: -0.1270,
   },
   {
        name: 'Buckingham Palace',
        lat: 51.5014,
        lng: -0.1419,
   },
   {
        name: 'London Eye',
        lat: 51.5033,
        lng: -0.1195,
    },
    {
        name: 'Tower of London',
        lat: 51.5081,
        lng: -0.0759,
    },
    {
        name: 'St Paul Cathedral',
        lat: 51.5138,
        lng: -0.0984,
    },
    {
        name: 'Westminster Abbey',
        lat: 51.4993,
        lng: -0.1273,
    },
    {
        name: 'Palace of Westminster',
        lat: 51.4995,
        lng: -0.1248,
    },
    {
        name: 'London Tower Bridge',
        lat: 51.5055,
        lng: -0.0754,
    },
    {
        name: 'London Dungeon',
        lat: 51.5027,
        lng: -0.1194,
    },
    {
        name: 'Kensington Palace',
        lat: 51.5058,
        lng: -0.1877,
    },
    {
        name: 'Tate Modern',
        lat: 51.5074,
        lng: -0.1001,
    },
    {
        name: 'London Natural History Museum',
        lat: 51.4967,
        lng: -0.1764,
    },
    {
        name: 'London National Gallery',
        lat: 51.5089,
        lng: -0.1283,
    },
    {
        name: 'St James Park',
        lat: 51.5025,
        lng: -0.1348,
    },
    {
        name: 'Sea Life London Aquarium',
        lat: 51.5020,
        lng: -0.1196,
    },
    {
        name: 'London HMS Belfast',
        lat: 51.5066,
        lng: -0.0814,
    },
    {
        name: 'London Hyde Park',
        lat: 51.5073,
        lng: -0.1657,
    }
];

/*
* @constructor
* @param {Object[]} Attractions
* @description Creates an instance of markerObject.
*/
function markerObject(a) {
	var self = this;
	
	self.name = a.name;
	self.lat = a.lat;
	self.long = a.lng;
    	self.description = "";

	self.visible = ko.observable(true);

	var wikiUrl = 'http://en.wikipedia.org/w/api.php?action=opensearch&search=' + a.name + '&format=json&callback=wikiCallback';
	
	$.ajax({
		url: wikiUrl,
		dataType: "jsonp",
    	}).done(function( response ) {
        	if ( response[2][1] == undefined ) {
            		self.description = "";
        	} else {
            		self.description = response[2][1];
        	}
    	}).fail(function() {
        	alert("Error in loading Wikimedia API");
    	});

	self.marker = new google.maps.Marker({
		position: new google.maps.LatLng(a.lat, a.lng),
		map: map,
		title: a.name
	});

    	self.contentString = '<div class="info-window-content"><div class="title"><b>' + a.name + "</b></div>" +
                    '<div class="content">' + self.description + "</div></div>";

	infoWindow = new google.maps.InfoWindow({content: self.contentString});

	self.marker.addListener('click', function(){
		self.contentString = '<div class="info-window-content"><div class="title"><b>' + a.name + "</b></div>" +
        '<div class="content">' + self.description + "</div><div>";

        infoWindow.setContent(self.contentString);

	infoWindow.open(map, this);

	self.marker.setAnimation(google.maps.Animation.BOUNCE);
      		setTimeout(function() {
      			self.marker.setAnimation(null);
     		}, 2100);
	});

	self.bounce = function(place) {
		google.maps.event.trigger(self.marker, 'click');
	};

    	self.showMarker = ko.computed(function() {
        	self.marker.setVisible(self.visible());
        	return true;
	}, this);
}

/*
* @description Initialize google maps.
*/
function initMap() {

    var uluru = {lat: 51.5074, lng: -0.1278};
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 13,
        center: uluru
    });
}

/*
* @description  Model-view-viewmodel of the app.
*/
function modelViewViewModel() {
	var self = this;
	self.attractionList = ko.observableArray([]);
	self.filterTerm = ko.observable('');

    	initMap();

    	Attractions.forEach( function( attraction ) {
        	self.attractionList.push( new markerObject(attraction) );
    	});

	self.filteredList = ko.computed( function() {
		var filter = self.filterTerm().toLowerCase();
		
		if (filter) {
            		return ko.utils.arrayFilter(self.attractionList(), function(attraction) {
				var result = (attraction.name.toLowerCase().search(filter) >= 0);
				attraction.visible(result);
				return result;
			});
		} else {
            		self.attractionList().forEach( function( a )  {
                		a.visible(true);
			});
			return self.attractionList();
		}
	}, self);
}

/*
* @description Error handling for Google maps
*/
function errorHandlingFunction() {
    alert("Error in loading Google MapsAPI.");
}

/*
* @description Initialize the app.
*/
function initialize() {
    ko.applyBindings(new modelViewViewModel());
}
