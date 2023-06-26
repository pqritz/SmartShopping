const searchInput = document.getElementById('search-input');
const dropdownMenu = document.getElementById('dropdown-menu');
const addItemMenu = document.getElementById("add-item-container");
const button = document.getElementById("cta-button");
const fBox = document.getElementById("FunctionalityBox");
const body = document.getElementById("bodyContainer");
const itemList = document.getElementById("items")

// Mock data for demonstration purposes
var allStores = jsonToArray()
var userLat = null;
var userLon = null;

searchInput.addEventListener('input', updateDropdownMenu);
//searchInput.addEventListener('click', showClosest);
document.addEventListener('click', hideDropdownMenu);
button.addEventListener('click', function (event) {
    event.preventDefault();
    fBox.style.display = "flex"
    document.body.style.opacity = 0.8

    for (let i = 0; i < fBox.children.length; i++) {
        fBox.children[i].style.display = 'initial'
    }
});


window.onload = function () {
    getLocation()
};

function updateDropdownMenu() {
    const searchTerm = searchInput.value;
    // You can perform your search logic here using the searchTerm

    // Clear previous results
    dropdownMenu.innerHTML = '';

    // Filter and display up to ten results
    const filteredResults = allStores.filter(item => item.uun.toLowerCase().includes(searchTerm.toLowerCase()));


    if (filteredResults.length === 0) {
        const li = document.createElement('li');
        li.textContent = 'No matching results found';
        li.classList.add('no-results');
        dropdownMenu.appendChild(li);
    } else {
        filteredResults.forEach(result => {
            result = result.uun;
            const li = document.createElement('li');
            li.textContent = result;
            li.addEventListener('click', () => {
                searchInput.value = result;
                updateItemMenu(searchInput.value)
                hideDropdownMenu();
            });
            dropdownMenu.appendChild(li);
        });
    }

    // Show the dropdown menu
    dropdownMenu.style.display = 'block';
    dropdownMenu.style.height = ((dropdownMenu.childNodes.length < 7) ? dropdownMenu.childNodes.length : 6) * dropdownMenu.childNodes[0].offsetHeight
}

function hideDropdownMenu() {
    dropdownMenu.style.display = 'none';
}

function showClosest() {
    getLocation()
    if (userLon == null && userLat == null) {
        alert("It seems that we couldnt get your Location")
    }
}

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        console.log("couldnt")
    }
}

function showPosition(position) {
    userLat = position.coords.latitude;
    userLon = position.coords.longitude;
}

function jsonToArray() {
    var storesFromArray = []
    getJson().then(Response => Response.json())
        .then(data => {
            data.Stores.forEach(element => {
                var newStore = {}
                newStore.brand = element.name
                newStore.uun = element.uun
                newStore.lon = element.longitude
                newStore.lat = element.latitude
                storesFromArray.push(newStore)
            });
        });
    return storesFromArray
}

function getJson() {
    return fetch("../json/Stores.json");
}

async function updateItemMenu(StoreUUN) {
    while (itemList.firstChild) {
        itemList.removeChild(itemList.firstChild)
    }
    StoreUUN = "Lidl, Nuernberger Str., Altdorf bei Nuernberg"
    grocery = await getGrocery(StoreUUN)
    if (grocery === null) {
        return
    }
    grocery.forEach(result => {
        const ul = document.createElement('ul');
        ul.textContent = result;
        ul.addEventListener('click', () => {
            liElements = ul.querySelectorAll('li')
            
            hideOtherMenus(ul)

            liElements.forEach(li => {
                ul.removeChild(li)
            })

            fullGrocery = getGroceryTypes(ul.textContent)
            console.log(fullGrocery)

            fullGrocery.forEach(element => {
                const li = document.createElement('li');
                const button = document.createElement('button')
    
                button.textContent = "+"
                button.className = "itemListButton"
    
                li.textContent = element[0]
                li.appendChild(button)
                ul.appendChild(li)
            })
        });
        itemList.appendChild(ul);
    });

}

function hideOtherMenus(ul) {

    itemList.childNodes.forEach(element => {
        if(element !== ul) {
            liElement = element.querySelectorAll('li')
            liElement.forEach(li => {
                element.removeChild(li)
            })
        }
    })
}

async function getGroceryUniqueIdentifier(StoreUUN) {
    try {
        const response = await getJson();
        const data = await response.json();
        const store = data.Stores.find(element => StoreUUN.toLowerCase() === element.uun.toLowerCase());
        if (store) {
            return store.items;
        }
        return undefined;
    } catch (error) {
        console.error(error);
        return undefined;
    }
}

async function getGrocery(StoreUUN) {
    const regex = /^[^0-9]*/;
    var newGrocery = [];

    try {
        const grocery = await getGroceryUniqueIdentifier(StoreUUN);
        if (grocery === undefined) {
            return;
        }

        grocery.forEach(element => {
            const newString = element.match(regex);
            if (newString) {
                newGrocery.push(newString[0]);
            }
        });
    } catch (error) {
        console.error(error);
    }

    const newList = Array.from(new Set(newGrocery));
    return newList;
}

async function getGroceryTypes(grocery) {
    try {
      const response = await fetch("../json/groceries.json");
      const data = await response.json();
  
      const list = [];
      data.grocery.forEach((element) => {
        if (element.ItemName.toLowerCase() === grocery.toLowerCase()) {
          element.Varieties.forEach((variety) => {
            const item = [];
            item.push(variety.Brand);
            item.push(variety.nutriScore);
            item.push(variety.data);
            list.push(item);
          });
        }
      });
  
      return list;
    } catch (error) {
      console.error(error);
      return []; // Return an empty array in case of an error
    }
  }
  