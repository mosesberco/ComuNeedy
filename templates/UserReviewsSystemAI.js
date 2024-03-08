describe("calculateRating", () => {
  // Test 1: Handles basic case with positive counts
  test("calculates total rating and rating based on stars correctly (positive counts)", () => {
    const data = [
      { star: 5, count: 100 },
      { star: 4, count: 200 },
      { star: 3, count: 300 },
    ];

    const result = calculateRating(data);

    expect(result.total_rating).toBe(600);
    expect(result.rating_based_on_stars).toBe(2200); // (5*100) + (4*200) + (3*300) = 2200
  });

  // Test 2: Handles zero count for a rating
  test("calculates total rating and rating based on stars correctly (zero count)", () => {
    const data = [
      { star: 5, count: 100 },
      { star: 4, count: 200 },
      { star: 3, count: 300 },
      { star: 2, count: 0 }, // Zero count for 2-star rating
      { star: 1, count: 500 },
    ];

    const result = calculateRating(data);

    expect(result.total_rating).toBe(1100); // Total count includes zero
    expect(result.rating_based_on_stars).toBe(2700); // (5*100) + (4*200) + (3*300) + (2*0) + (1*500) = 2700
  });

  // Test 3: Handles null or undefined count values (if applicable)
  // Update this test based on how your `calculateRating` function handles null/undefined counts
  test("throws error for null or undefined count values (if applicable)", () => {
    const invalidData = [
      { star: 5, count: 100 },
      { star: 4, count: null }, // Null count
      { star: 3, count: 300 },
    ];

    expect(() => calculateRating(invalidData)).toThrowError(
      "Count value is null or undefined"
    ); // Modify error message if different
  });
});
