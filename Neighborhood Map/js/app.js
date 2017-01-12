var map;
var markers = [];

this.attractions = [
    'London Eye', 51.5033, -0.1195, 'L'],
    ['Tower of London', 51.5081, -0.0759, 'T'],
    ['St Paul Cathedral', 51.5138, -0.0984, 'P'],
    ['Buckingham Palace', 51.5014, -0.1419, 'B'],
    ['Westminster Abbey', 51.4993, -0.1273, 'W'],
    ['Big Ben', 51.5007, -0.1246, 'B'],
    ['British Museum', 51.5194, -0.1270, 'B'],
    ['Palace of Westminster', 51.4995, -0.1248, 'P'],
    ['Tower Bridge', 51.5055, -0.0754, 'T'],
    ['London Dungeon', 51.5025, -0.1188, 'L'],
    ['Kensington Palace', 51.5058, -0.1877, 'K'],
    ['Tate Modern', 51.5074, -0.1001, 'T'],
    ['Natural History Museum', 51.4967, -0.1764, 'N'],
    ['National Gallery', 51.5089, -0.1283, 'N'],
    ['St James Park', 51.5025, -0.1348, 'J'],
    ['Sea Life London Aquarium', 51.5020, -0.1196, 'S'],
    ['HMS Belfast', 51.5066, -0.0814, 'H'],
    ['Hyde Park', 51.5073, -0.1657, 'H'],
    ['London Aquarium', 51.5020, -0.1196, 'A']
];

function initMap() {

    var self = this;

    var uluru = {lat: 51.5074, lng: -0.1278};

    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 13,
        center: uluru
    });
    marker = new google.maps.Marker({
        position: uluru,
        map: map
    });

    for( var i = 0; i < attractions.length; i++ ) {
        addMarker(attractions[i]);
    }
};

function addMarker(m) {

    var title = m[0];
    var pos = new google.maps.LatLng(m[1], m[2]);
    var cat = m[3];

    tempMarker = new google.maps.Marker({
        title: title,
        position: pos,
        category: cat,
        map: map
    });

    tempMarker.setAnimation(null);

    (function(tempMarker) {
        google.maps.event.addListener(tempMarker, "click", function(e) {
            if (tempMarker.getAnimation() !== null ) {
                tempMarker.setAnimation(null);
            } else {
                tempMarker.setAnimation(google.maps.Animation.BOUNCE);
            }
        })
    })(tempMarker);

    markers.push(tempMarker);
}


filterMarkers = function(cat) {
    for (var j = 0; j < attractions.length; j++) {
        marker = markers[j];
        if (marker.category == cat || cat.length == 0 ) {
            marker.setVisible(true);
        } else {
            marker.setVisible(false);
        }
    }
}

function ViewModel() {

}

function loadScript() {
    var link = "https://maps.googleapis.com/maps/api/js?callback=initMap";

    var jscript = document.createElement('script');
    jscript.type = "text/javascript"
    jscript.src = link;
    jscript.async;
    jscript.defer;
    document.getElementsByTagName('body')[0].appendChild(jscript);
};

ko.applyBindings(new ViewModel());
ko.applyBindings(new loadScript());

/*
function myFunction() {
    var input, filter, ul, li, a, i;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    ul = document.getElementById("myUL");
    li = ul.getElementsByTagName("li");
    for (i = 0; i < li.length; i++) {
        a = li[i].getElementsByTagName("a")[0];
        if (a.innerHTML.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}

    this.attractions = ko.observableArray([
        'Big Ben',
        'British Museum',
        'Buckingham Palace',
        'HMS Belfast',
        'Hyde Park',
        'Kensington Palace',
        'London Aquarium',
        'London Dungeon',
        'London Eye',
        'National Gallery',
        'Natural History Museum',
        'Palace of Westminster',
        'Sea Life London Aquarium',
        'St James Park',
        'St Paul Cathedral',
        'Tower of London',
        'Tower Bridge',
        'Tate Modern',
        'Westminster Abbey'
    ]);
*/