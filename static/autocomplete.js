// new autoComplete({
//     data: {                              // Data src [Array, Function, Async] | (REQUIRED)
//       src: films,
//     },
//     selector: "#autoComplete",
//     resultsList: {                       // Rendered results list object      | (Optional)
//         render: true,
//         container: source => {
//             source.setAttribute("id", "autoComplete");
//         },
//         destination: document.querySelector("#autoComplete"),
//         position: "afterend",
//         element: "ul"
//     },
//     maxResults: 5,                         // Max. number of rendered results | (Optional)
//     highlight: true, 
//     resultItem: {                          // Rendered result item            | (Optional)
//         content: (data, source) => {
//             source.innerHTML = data.match;
//         },
//         element: "li"
//     },
//     noResults: () => {                     // Action script on noResults      | (Optional)
//         const result = document.createElement("li");
//         result.setAttribute("class", "no_result");
//         result.setAttribute("tabindex", "1");
//         result.innerHTML = "No Results";
//         document.querySelector("#autoComplete_list").appendChild(result);
//     },
//     onSelection: feedback => {             // Action script onSelection event | (Optional)
//         document.getElementById('autoComplete').value = feedback.selection.value;
//     }
// });