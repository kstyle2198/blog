
// select elements
const iconElement = document.querySelector('.weather-icon');
const tempElement = document.querySelector('.temperature-value p');
const descElement = document.querySelector('.temperature-description p');
const locationElement = document.querySelector('.location p');
const notificationElement = document.querySelector('.notification');

// App data
const weather1 = {};
weather1.temperature = {
  unit: 'celsius',
};

// App Const and vars
const KELVIN = 273;

// API KEY
const key = 'b628a7d2c27f2ee337e0c0cfe94f6277';

// check if browser support geolocation
if ('geolocation' in navigator) {
  navigator.geolocation.getCurrentPosition(setPosition, showError);
} else {
  notificationElement.style.display = 'block';
  notificationElement.innerHtml =
    '<p>Browser does not support you Geolocation</p>';
}

// set user's postion

function setPosition(position) {
  let latitude = position.coords.latitude;
  let longitude = position.coords.longitude;
  console.log(latitude, longitude)

  getWeather(latitude, longitude);
}

// show error

function showError(error) {
  notificationElement.style.display = 'block';
  notificationElement.innerHTML = `<p> ${error.message} </p>`;
}

//get weather fuction
function getWeather(latitude, longitude) {
  let api = `https://api.openweathermap.org/data/2.5/weather?lat=${latitude}&lon=${longitude}&appid=${key}`;
  //   console.log(api);
  fetch(api)
    .then(function (response) {
      let data = response.json();
      return data;
    })
    .then(function (data) {
      weather1.temperature.value = Math.floor(data.main.temp - KELVIN);
      weather1.description = data.weather[0].description;
      weather1.iconId = data.weather[0].icon;
      weather1.city = data.name;
      weather1.country = data.sys.country;
    })
    .then(function () {
      displayWeather();
    });
}

// display weather to UI
function displayWeather() {
  iconElement.innerHTML = `<img src="/media/icons/${weather1.iconId}.png"/>`;
  tempElement.innerHTML = `${weather1.temperature.value}°<span>C</span>`;
  descElement.innerHTML = `${weather1.description}`;
  locationElement.innerHTML = `${weather1.city}, ${weather1.country}`;
}

// C to F conversion
function celsiusToFahrenheit(temperature) {
  return (temperature * 9) / 5 + 32;
}

// WHEN THE USER CLICKS ON THE TEMPERATURE ELEMENET
tempElement.addEventListener('click', function () {
  if (weather1.temperature.value === undefined) return;

  if (weather1.temperature.unit == 'celsius') {
    let fahrenheit = celsiusToFahrenheit(weather1.temperature.value);
    fahrenheit = Math.floor(fahrenheit);

    tempElement.innerHTML = `${fahrenheit}°<span>F</span>`;
    weather1.temperature.unit = 'fahrenheit';
  } else {
    tempElement.innerHTML = `${weather1.temperature.value}°<span>C</span>`;
    weather1.temperature.unit = 'celsius';
  }
});
