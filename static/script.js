var selectedRow = null;

//show alerts
function showAlert(message, className) {
  const div = document.createElement("div");
  div.className = `alert alert-${className}`;

  div.appendChild(document.createTextNode(message));
  const container = document.querySelector(".container");
  const main = document.querySelector(".main");
  container.insertBefore(div, main);

  setTimeout(() => document.querySelector(".alert").remove(), 3000);
  
}

//clear all fields
function clearFields(){
    document.querySelector("#personalName").value = "";
    document.querySelector("#personalGender").value = "";
    document.querySelector("#personalAge").value = "";
    document.querySelector("#personalCountry").value = "";
}

//add data

document.querySelector("#jobs-form").addEventListener("submit", (e) =>{
    e.preventDefault();

    //get form values
    const personal_name = document.querySelector("#personalName").value;
    const personal_gender = document.querySelector("#personalGender").value;
    const personal_age = document.querySelector("#personalAge").value;
    const personal_country = document.querySelector("#personalCountry").value;

    //validate
    if(personal_name == "" || personal_gender == "" || personal_age == "" || personal_country == ""){
        showAlert("Please, fill in all fields!");
    }
    else{
        if(selectedRow == null){
            const list = document.querySelector("#job-list");
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${personal_name}</td>
                <td>${personal_gender}</td>
                <td>${personal_age}</td>
                <td>${personal_country}</td>
                <td>
                <a href="#" class="btn btn-warning btn-sm edit">Edit</a>
                <a href="#" class="btn btn-danger btn-sm delete">Delete</a>
                </td>
            `;
            list.appendChild(row);
            selectedRow = null;
            showAlert("People added!")
        }
        else{
            selectedRow.children[0].textContent = personal_name;
            selectedRow.children[1].textContent = personal_gender;
            selectedRow.children[2].textContent = personal_age;
            selectedRow.children[3].textContent = personal_country;
            selectedRow = null;
            showAlert("People Info Edited", "info");


        }
        clearFields();
    }

});

//edit data

document.querySelector("#job-list").addEventListener("click", (e) =>{
    target = e.target;
    if(target.classList.contains("edit")){
        selectedRow = target.parentElement.parentElement;
        document.querySelector("#personalName").value = selectedRow.children[0].textContent;
        document.querySelector("#personalGender").value = selectedRow.children[1].textContent;
        document.querySelector("#personalAge").value = selectedRow.children[2].textContent;
        document.querySelector("#personalCountry").value = selectedRow.children[3].textContent;
    }
});

// delete data

document.querySelector("#job-list").addEventListener("click", (e) =>{
    target = e.target;
    if(target.classList.contains("delete")){
        target.parentElement.parentElement.remove();
        showAlert("Job data deleted! Danger!");
    }

});