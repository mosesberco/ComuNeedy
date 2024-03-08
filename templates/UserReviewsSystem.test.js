// Import the function to be tested
const { calculateRating } = require("./UserReviewsSystem");

describe("calculateRating", () => {
  test("calculates total rating and rating based on stars correctly", () => {
    // data for example
    const data = [
      { star: 5, count: 100 },
      { star: 4, count: 200 },
      { star: 3, count: 300 },
      { star: 2, count: 400 },
      { star: 1, count: 500 },
    ];

    // Call function
    const result = calculateRating(data);

    // Check values
    expect(result.total_rating).toBe(1500);
    expect(result.rating_based_on_stars).toBe(3500); // (5*100) + (4*200) + (3*300) + (2*400) + (1*500) = 3500
  });
});
