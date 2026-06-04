const images = document.querySelectorAll(".preview-img");
const viewer = document.getElementById("imageViewer");
const viewerImg = document.getElementById("viewerImage");

let currentIndex = 0;

// Open viewer
images.forEach((img, index) => {
    img.addEventListener("click", () => {
        currentIndex = index;
        showImage();
        viewer.style.display = "flex";
    });
});

// Show image
function showImage() {
    viewerImg.src = images[currentIndex].src;
}

// Close
document.querySelector(".close-btn").onclick = () => {
    viewer.style.display = "none";
};

// Next
document.querySelector(".right").onclick = () => {
    currentIndex = (currentIndex + 1) % images.length;
    showImage();
};

// Previous
document.querySelector(".left").onclick = () => {
    currentIndex = (currentIndex - 1 + images.length) % images.length;
    showImage();
};


// Keyboard Navigation

document.addEventListener("keydown", (e) => {
    if (viewer.style.display === "flex") {
        if (e.key === "ArrowRight") {
            document.querySelector(".right").click();
        }
        if (e.key === "ArrowLeft") {
            document.querySelector(".left").click();
        }
        if (e.key === "Escape") {
            viewer.style.display = "none";
        }
    }
});

const stars = document.querySelectorAll("#rating-stars span");
const ratingValue = document.getElementById("rating-value");
const ratingInput = document.getElementById("rating-input");

let selectedRating = 0;

stars.forEach(star => {
    star.addEventListener("click", function () {
        selectedRating = this.getAttribute("data-value");

        ratingInput.value = selectedRating;
        ratingValue.textContent = selectedRating;

        updateStars(selectedRating);
    });
});

function updateStars(value) {
    stars.forEach(star => {
        if (star.getAttribute("data-value") <= value) {
            star.classList.add("active");
        } else {
            star.classList.remove("active");
        }
    });
}

