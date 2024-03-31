// Define functions
function calculateRating(data) {
  if (!data) {
    throw new Error("Data is undefined or null");
  }

  let total_rating = 0;
  let rating_based_on_stars = 0;

  data.forEach((rating) => {
    if (rating.count != null) {
      total_rating += rating.count;
      rating_based_on_stars += rating.count * rating.star;
    } else {
      throw new Error("Count value is null or undefined");
    }
  });

  return { total_rating, rating_based_on_stars };
}
async function getRating() {
  const response = await fetch("/api/avg_reviews");
  if (response.ok) {
    const ratingData = await response.json();
    return ratingData;
  } else {
    throw new Error("Failed to fetch rating data");
  }
}

function generateRatingHTML(data) {
  let total_rating = 0;

  data.forEach((rating) => {
    total_rating += rating.count;
  });

  let ratingHTML = "";

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
    ratingHTML += rating_progress;
  });

  return ratingHTML;
}
// Attach event listener to DOMContentLoaded
document.addEventListener("DOMContentLoaded", function () {
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
      count: 20,
    },
    {
      star: 2,
      count: 10070,
    },
    {
      star: 1,
      count: 25020,
    },
  ];

  let ratingHTML = generateRatingHTML(data);

  let { total_rating, rating_based_on_stars } = calculateRating(data);

  let rating_average = (rating_based_on_stars / total_rating).toFixed(1);

  // Update the calculated ratings
  document.querySelector(".rating__average h1").innerHTML = rating_average;
  document.querySelector(".rating__average p").innerHTML =
    total_rating.toLocaleString();
  document.querySelector(".rating__progress").innerHTML = ratingHTML;
  document.querySelector(".star-inner").style.width =
    (rating_average / 5) * 100 + "%";
});
module.exports = { calculateRating, generateRatingHTML };
