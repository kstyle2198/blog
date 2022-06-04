const weather = document.querySelector('.js-weather');

const API_KEY = 'b628a7d2c27f2ee337e0c0cfe94f6277';
const COORDS = 'coords';

function getWeather(lat, lng) {
  fetch(
    `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lng}&appid=${API_KEY}&units=metric`
  )
    .then(function (response) {
      // console.log(response.json());
      return response.json();
    })
    .then(function (json) {
      // console.log(json);
      const temperature = json.main.temp;
      const condition = json.weather[0].description;
      const icon = json.weather[0].icon;
      console.log(condition);
      const place = json.name;
      console.log(place);
      weather.innerText = `${condition} (${temperature}℃) @ ${place}`;
    });
}


function saveCoords(coordsObj) {
  localStorage.setItem(COORDS, JSON.stringify(coordsObj));
}

function handleGeoSuccess(position) {
  const latitude = position.coords.latitude;
  const longitude = position.coords.longitude;
  const coordsObj = {
    latitude: latitude,
    longitude: longitude,
  };
  saveCoords(coordsObj);
  getWeather(latitude, longitude);
}

function handleGeoError() {
  console.log("Can't access geo location");
}

function askForCoords() {
  navigator.geolocation.getCurrentPosition(handleGeoSuccess, handleGeoError);
}


function loadCoords() {
  const loadedCoords = localStorage.getItem(COORDS);
  if (loadedCoords === null) {
    askForCoords();
  } else {
    const parseCoords = JSON.parse(loadedCoords);
    // console.log(parseCoords);
    getWeather(parseCoords.latitude, parseCoords.longitude);
  }
}

function init() {
  loadCoords();
}

init();
