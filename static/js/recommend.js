document.addEventListener("DOMContentLoaded", function() {
    // Hide the loader when the page has fully loaded
    document.getElementById('loader-container').classList.add('hidden');
  });

  function openMovieDetailsPage(movieid) {
    document.getElementById('loader-container').classList.remove('hidden'); // Show the loader

    // Add a short delay to allow the loader to appear before redirecting
    setTimeout(function() {
      window.location.href = '/movie_page/' + movieid;
    }, 100); // 100 milliseconds delay
  }

  function handleFormSubmit() {
    const selectedMovie = document.getElementById('movies').value;
    if (selectedMovie === '') {
      return false;
    }
    document.getElementById('loader-container').classList.remove('hidden'); // Show the loader

    // Allow form submission to proceed normally
    return true;
  }

  // Initialize AOS
  AOS.init();