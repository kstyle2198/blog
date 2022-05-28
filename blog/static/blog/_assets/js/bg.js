
const body = document.querySelector('body');
const IMG_NUMBER = 5;
// const UNSPLASH_URL = `https://api.unsplash.com/photos/random?client_id=9zoCbwz1ZgC0Ss_ashtbCy-8vURZdGbm8D6hZ4Ak7vA&query=landscape&orientation=landscape`;



function paintImage(imgNumber) {
  const image = new Image();
  image.src = `/static/images/${imgNumber + 1}.jpg`;
  image.classList.add('bgimage'); // CSS와 연결
  body.prepend(image);
}

function genRandom() {
  const number = Math.floor(Math.random() * IMG_NUMBER); // floor는 소수점 버림
  return number;
}

function init() {
  const randomNumber = genRandom();
  paintImage(randomNumber);
}

init();
