const searchInput = document.getElementById('search-input');
const dropdownMenu = document.getElementById('dropdown-menu');
const addItemMenu = document.getElementById("add-item-container");
const body = document.getElementById("bodyContainer");
const itemList = document.getElementById("items")
const itemSearch = document.getElementById("search-item-input")

var allStores = jsonToArray()

var shoppingList = []

searchInput.addEventListener('input', updateDropdownMenu);
document.addEventListener('click', hideDropdownMenu);
itemSearch.addEventListener('input', updateItemList);

async function updateItemList() {
    var StoreUUN = searchInput.value
    var filtered = allStores.filter(item => item.uun.toLowerCase() == StoreUUN.toLowerCase())
    if (filtered.length != 1) {
        return
    }

    grocery = await getGrocery(StoreUUN)
    if (grocery === null) {
        return
    }

    var filteredResults = undefined

    if (itemSearch.value.length > 0) {
        filteredResults = grocery.filter(item => item.toLowerCase().includes(itemSearch.value.toLowerCase()));
    } else {
        filteredResults = grocery
    }

    Array.from(itemList.children).forEach(element => {
        if (filteredResults.includes(element.textContent.slice(0, -1).toLowerCase())) {
            element.style.display = 'block'
        } else {
            element.style.display = 'none'
        }
    })

    console.log(shoppingList)
}

function updateDropdownMenu() {
    itemSearch.style.display = 'none'
    itemSearch.style.pointerEvents = 'none'
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
    itemSearch.style.display = 'initial'
    itemSearch.style.pointerEvents = 'initial'
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

function makeUpperCase(str) {
    const indexOfFirst = str.search(/[a-zA-Z]/)
    if (indexOfFirst !== -1) {
        const modifiedStr = str.slice(0, indexOfFirst) + str.charAt(indexOfFirst).toUpperCase() + str.slice(indexOfFirst + 1);
        return modifiedStr
    } else {
        return str
    }
}

async function updateItemMenu(StoreUUN) {
    while (itemList.firstChild) {
        itemList.removeChild(itemList.firstChild)
    }
    grocery = await getGrocery(StoreUUN)
    if (grocery === null) {
        return
    }


    const searchTerm = itemSearch.value

    var filteredResults = undefined

    if (searchTerm.length > 0) {
        filteredResults = grocery.filter(item => item.toLowerCase().includes(searchTerm.toLowerCase()));
    } else {
        filteredResults = grocery
    }


    grocery.forEach(result => {
        const ul = document.createElement('ul');
        ul.calssName = "ulGroceries"
        ul.textContent = makeUpperCase(result);
        ul.addEventListener('click', async () => {
            //ul.style.fontWeight = "bold"
            liElements = ul.querySelectorAll('li')

            grocery = await getGroceryUniqueIdentifier(ul.textContent)

        });
        const button = document.createElement('button')
        const span = document.createElement("span")
        button.value = "true"
        span.textContent = "+"
        button.appendChild(span)
        button.className = "itemListButton"

        button.onclick = function (event) {

            if (button.value === "true") {
                button.value = "false"
                button.style.backgroundColor = "#AF504C"
                button.ontoggle
                span.textContent = "-"
                shoppingList.push(button.parentElement.textContent.slice(0, -1))
            } else {
                button.value = "true"
                button.style.backgroundColor = "#4CAF50"
                span.textContent = "+"
                shoppingList.splice(shoppingList.indexOf(button.parentElement.textContent.slice(0, -1)), 1)
            }

            itemSearch.value = ""
            Array.from(itemList.children).forEach(element => {
                element.style.display = 'block'

            })
        }

        if (!filteredResults.includes(result)) {
            ul.style.display = 'none'
        } else {
            ul.style.display = 'block'
        }

        ul.appendChild(button)
        itemList.appendChild(ul);
    });

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
        return grocery
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


function addMarkerToImage(path, points, color, size, fontSize) {
    const image = new Image();
    image.onload = function () {
        const canvas = document.createElement('canvas');
        canvas.width = image.width;
        canvas.height = image.height;
        const context = canvas.getContext('2d');

        context.drawImage(image, 0, 0);

        for (const p of points) {
            addMarker(context, p, color, size, '', [0, 0], fontSize);
        }

        const imageDataURL = canvas.toDataURL('image/png');

        const imgElement = document.createElement('img');
        imgElement.src = imageDataURL;

        document.body.appendChild(imgElement);
    };

    image.src = path;
}

function addMarker(context, position, color, size, text, textPos, fontSize) {
    const [markerX, markerY] = position;
    const [textX, textY] = textPos;

    context.font = `${fontSize}px Arial`;
    context.fillStyle = 'white';
    context.fillText(text, textX, textY);

    const { width, height } = context.canvas;
    const markerRadius = size * Math.min(width, height);
    const markerCenterX = markerX * width;
    const markerCenterY = markerY * height;
    const markerStartAngle = Math.PI;
    const markerEndAngle = 0;

    context.beginPath();
    context.arc(markerCenterX, markerCenterY, markerRadius, markerStartAngle, markerEndAngle);
    context.fillStyle = color;
    context.fill();

    const triangleSize = size * Math.min(width, height);

    context.beginPath();
    context.moveTo(markerCenterX, markerCenterY + triangleSize * 2);
    context.lineTo(markerCenterX - triangleSize, markerCenterY);
    context.lineTo(markerCenterX + triangleSize, markerCenterY);
    context.closePath();
    context.fillStyle = color;
    context.fill();
}

function renderImage() {
    // Example usage
    const imagePath = '../json/stores/Lidl, Nuernberger Str., Altdorf bei Nuernberg.png';
    const markerPoints = [[0.5, 0.5], [0.3, 0.7], [1, 1], [0.8, 0.2]];
    const markerColor = '#FF0000';
    const markerSize = 0.02;
    const markerFontSize = 18;

    addMarkerToImage(imagePath, markerPoints, markerColor, markerSize, markerFontSize);
}