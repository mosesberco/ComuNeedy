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

const userDetails =JSON.parse(sessionStorage.getItem('user'));
document.getElementById('name').value = userDetails.name;
document.getElementById('email').value = userDetails.email;
const requestDetails = JSON.parse(sessionStorage.getItem('request'));
async function send_review(){

    const comment = document.getElementById('comment').value;

  // Count the number of active stars
  const stars = document.querySelectorAll(".stars i.active").length;
  const reviewData = {
    "name": userDetails.name + " "+userDetails.last_name,
    "email": userDetails.email,
    "comment": comment,
    "stars": stars,
    "request_id": requestDetails.request_id
  };
  const response = await fetch("/api/update_review",{
            method: 'POST',
            headers: {
                        'Content-Type': 'application/json'
                    },
            body: JSON.stringify(reviewData)
                   });
  if (response.ok)
  {
  console.log("added");
  window.location.href = "My_requests.html";
  document.getElementById('comment').value = '';
  console.log("go back");
  window.location.href = "My_requests.html";
  }
}
