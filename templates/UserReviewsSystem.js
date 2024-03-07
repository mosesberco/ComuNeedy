let data = [
  {
    star: 5,
    count: 99980,
  },
  {
    star: 4,
    count: 39300,
  },
  {
    star: 3,
    count: 25050,
  },
  {
    star: 2,
    count: 10070,
  },
  {
    star: 1,
    count: 5020,
  },
];

let total_rating = 0,
  rating_based_on_stars = 0;

data.forEach((rating) => {
  total_rating += rating.count;
  rating_based_on_stars += rating.count * rating.star;
});

data.forEach((rating) => {
  let rating_progress = `
        <div class="rating__progress-value">
          <p>${rating.star} <span class="star">&#9733;</span></p>
          <div class="progress">
            <div class="bar" style="width: ${
              (rating.count / total_rating) * 100
            }%;"></div>
          </div>
          <p>${rating.count.toLocaleString()}</p>
        </div> 
      `;
  document.querySelector(".rating__progress").innerHTML += rating_progress;
});

let rating_average = (rating_based_on_stars / total_rating).toFixed(1);
document.querySelector(".rating__average h1").innerHTML = rating_average;
document.querySelector(".rating__average p").innerHTML =
  total_rating.toLocaleString();
document.querySelector(".star-inner").style.width =
  (rating_average / 5) * 100 + "%";
