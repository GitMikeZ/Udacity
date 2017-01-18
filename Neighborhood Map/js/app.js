// Map variable
var map;

// Attraction array to display on google map with name, longitude, and latitude
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

// Marker object to place on the map
function markerObject(a) {
	var self = this;

    this.name = a.name;
	this.lat = a.lat;
	this.long = a.lng;
    this.description = "";

	this.visible = ko.observable(true);

    var wikiUrl = 'http://en.wikipedia.org/w/api.php?action=opensearch&search=' + a.name + '&format=json&callback=wikiCallback';

    $.ajax({
        url: wikiUrl,
        dataType: "jsonp",
        success: function( response ) {
                self.description = response[2][1];
        }
    })

	this.contentString = '<div class="info-window-content"><div class="title"><b>' + a.name + "</b></div>" +
                        '<div class="content">' + self.description + "</div></div>";

	this.infoWindow = new google.maps.InfoWindow({content: self.contentString});

	this.marker = new google.maps.Marker({
			position: new google.maps.LatLng(a.lat, a.lng),
			map: map,
			title: a.name
	});

	this.marker.addListener('click', function(){
		self.contentString = '<div class="info-window-content"><div class="title"><b>' + a.name + "</b></div>" +
        '<div class="content">' + self.description + "</div><div>";

        self.infoWindow.setContent(self.contentString);

		self.infoWindow.open(map, this);

		self.marker.setAnimation(google.maps.Animation.BOUNCE);
      	setTimeout(function() {
      		self.marker.setAnimation(null);
     	}, 5000);
	});

	this.bounce = function(place) {
		google.maps.event.trigger(self.marker, 'click');
	};

    this.showMarker = ko.computed(function() {
        if(this.visible()) {
            this.marker.setMap(map);
        } else {
            this.marker.setMap(null);
        }
        return true;
	}, this);
};

// Initialize the Google map centering at uluru
function initMap() {

    var uluru = {lat: 51.5074, lng: -0.1278};
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 13,
        center: uluru
    });
};

// Model-view-viewmodel of the app
function modelViewViewModel() {
	var self = this;
    this.attractionList = ko.observableArray([]);
	this.filterTerm = ko.observable("");

    initMap();

	for( var i = 0; i < Attractions.length; i++ ) {
        self.attractionList.push( new markerObject(Attractions[i]));
    };

	this.filteredList = ko.computed( function() {
		var filter = self.filterTerm().toLowerCase();
		if (filter) {
            return ko.utils.arrayFilter(self.attractionList(), function(attraction) {
				var result = (attraction.name.toLowerCase().search(filter) >= 0);
				attraction.visible(result);
				return result;
			});
		} else {
            for( var j = 0; j < self.attractionList.length; j++ ) {
                self.attractionList[j].visible(true);
            }
			return self.attractionList();
		}
	}, self);
};

// Initialize the app
function initialize() {
    ko.applyBindings(new modelViewViewModel());
}


