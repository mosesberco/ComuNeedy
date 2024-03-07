const stars = document.querySelectorAll(".stars i");
console.log(stars);

//Loop Through the start nodes

stars.forEach((star, index1) => {
  star.addEventListener("click", () => {
    console.log(index1);

    //Loop Through the start nodes
    stars.forEach((star, index2) => {
      index1 >= index2
        ? star.classList.add("active")
        : star.classList.remove("active");
    });
  });
});
