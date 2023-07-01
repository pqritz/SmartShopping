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

var shoppingList = []

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
    console.log(grocery)
    grocery.forEach(result => {
        const ul = document.createElement('ul');
        ul.textContent = result;
        ul.addEventListener('click', async () => {
            ul.style.fontWeight = "bold"
            liElements = ul.querySelectorAll('li')

            grocery = await getGroceryUniqueIdentifier(ul.textContent)

            /*hideOtherMenus(ul)

            liElements.forEach(li => {
                ul.removeChild(li)
            })



            await getGroceryTypes(ul.textContent).then(array => {
                fullGrocery = array
            })


            fullGrocery.forEach(element => {
                const li = document.createElement('li');
                const button = document.createElement('button')

                li.className = "groceryBrands"
                button.textContent = "+"
                button.className = "itemListButton"

                button.onclick = function (event) {
                    shoppingList.push(button.parentElement.textContent.slice(0, -1))
                    ul.removeChild(li)
                    console.log(shoppingList)
                }

                li.textContent = element[0]
                li.appendChild(button)
                ul.appendChild(li)
            })*/
        });
        itemList.appendChild(ul);
    });

}

function hideOtherMenus(ul) {

    itemList.childNodes.forEach(element => {
        if (element !== ul) {
            liElement = element.querySelectorAll('li')
            liElement.forEach(li => {
                element.removeChild(li)
            })
            element.style.fontWeight = "normal"
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
    const regex = /\d/;
    var newGrocery = [];

    try {
        const grocery = await getGroceryUniqueIdentifier(StoreUUN);
        return getGrocery
        /*
        if (grocery === undefined) {
            return;
        }
        for (let i = 0; i < grocery[0].length; i++) {
            let element = grocery[0][i].toString(); // Convert element to string
            const match = element.search(regex);
            const result = match !== -1 ? element.substring(0, match) : element;
            newGrocery.push(result);
        }*/
    } catch (error) {
        console.error(error);
    }

    //const newList = Array.from(new Set(newGrocery));
    //return newList;
}

function getGroceryTypes(grocery) {
    try {
        return fetch("../json/groceries.json")
            .then(response => response.json())
            .then(data => {
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
            })
            .catch(error => {
                console.error(error);
                return []; // Return an empty array in case of an error
            });
    } catch (error) {
        console.error(error);
        return []; // Return an empty array in case of an error
    }
}

async function runScript(pathToImage, points, color, size, pathOut, fontSize) {
    const path = "../../imageEditor/main.py"
    const scriptArgs = [pathToImage, points, color, size, pathOut, fontSize]

    try {
        const response = await fetch(pythonEndpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(scriptArgs)
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.status} ${response.statusText}`);
        }

        const output = await response.text();
        console.log('Python script output:', output);
    } catch (error) {
        console.error('An error occurred:', error);
    }
}