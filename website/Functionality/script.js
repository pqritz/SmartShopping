const searchInput = document.getElementById('search-input');
const dropdownMenu = document.getElementById('dropdown-menu');
const addItemMenu = document.getElementById("add-item-container");
const body = document.getElementById("bodyContainer");
const itemList = document.getElementById("items")
const itemSearch = document.getElementById("search-item-input")
const submitButton = document.getElementById('submit')
const backButton = document.getElementById("back-button")

var allStores = jsonToArray()

var shoppingList = []

searchInput.addEventListener('input', updateDropdownMenu);
document.addEventListener('click', hideDropdownMenu);
itemSearch.addEventListener('input', updateItemList);
itemSearch.addEventListener('focus', disableZoomOnInputFocus)
itemSearch.addEventListener('blur', enableZoomOnInputBlur)
submitButton.addEventListener('click', renderImage)
backButton.addEventListener('click', function (event) {
    window.location.href = '../../MainPage.html'
})

function disableZoomOnInputFocus() {
    var viewportMeta = document.querySelector('meta[name="viewport"]');
    if (viewportMeta) {
        viewportMeta.content = "width=device-width, initial-scale=1, maximum-scale=1, user-scalable=0";
    }
}

// Enable zooming after input field blur
function enableZoomOnInputBlur() {
    var viewportMeta = document.querySelector('meta[name="viewport"]');
    if (viewportMeta) {
        viewportMeta.content = "width=device-width, initial-scale=1";
    }
}

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
    groceryKeys = Object.keys(grocery)

    if (itemSearch.value.length > 0) {
        filteredResults = groceryKeys.filter(item => item.toLowerCase().includes(itemSearch.value.toLowerCase()));
    } else {
        filteredResults = groceryKeys
    }

    Array.from(itemList.children).forEach(element => {
        if (filteredResults.includes(element.textContent.slice(2, -1).toLowerCase())) {
            element.style.display = 'block'
        } else {
            element.style.display = 'none'
        }
    })
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

    groceryKeys = Object.keys(grocery)
    const searchTerm = itemSearch.value
    var filteredResults = undefined

    if (searchTerm.length > 0) {
        filteredResults = groceryKeys.filter(item => item.toLowerCase().includes(searchTerm.toLowerCase()));
    } else {
        filteredResults = groceryKeys
    }


    groceryKeys.forEach(result => {
        const ul = document.createElement('ul');
        ul.calssName = "ulGroceries"
        ul.textContent = grocery[result].emoji + makeUpperCase(result);
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
                if (shoppingList.length != 0) {
                    submitButton.style.display = 'initial'
                }
            } else {
                button.value = "true"
                button.style.backgroundColor = "#4CAF50"
                span.textContent = "+"
                shoppingList.splice(shoppingList.indexOf(button.parentElement.textContent.slice(0, -1)), 1)
                if (shoppingList.length == 0) {
                    submitButton.style.display = 'none'
                }
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

    } catch (error) {
        console.error(error);
    }
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

        const overlayImage = document.createElement('img');
        const button = document.createElement('button')
        const span = document.createElement('span')

        overlayImage.src = imageDataURL;
        overlayImage.alt = 'Overlay Image';
        overlayImage.id = 'overlayImage';
        overlayImage.style.position = 'fixed';
        overlayImage.style.top = '0';
        overlayImage.style.left = '0';
        overlayImage.style.width = '100%';
        overlayImage.style.height = '100%';
        overlayImage.style.objectFit = 'contain';
        overlayImage.style.objectPosition = 'center';
        overlayImage.style.zIndex = '9999';

        // Check if the image doesn't cover the entire site
        if (window.innerWidth > overlayImage.naturalWidth || window.innerHeight > overlayImage.naturalHeight) {
            // Add a white background behind the image
            overlayImage.style.backgroundColor = 'white';
        }


        button.className = 'back-button'
        button.textContent = ' Back'
        button.addEventListener('click', function (event) {
            overlayImage.remove()
        })

        span.className = 'arrow'

        // Append the overlay image element to the document body
        button.prepend(span)
        document.body.appendChild(overlayImage);
        document.body.appendChild(button)
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

function getImageSize(imageUrl) {
    return new Promise((resolve, reject) => {
        const img = new Image();

        img.onload = function () {
            resolve({ width: this.width, height: this.height});
        };

        img.onerror = function () {
            reject(new Error("Failed to load the image"));
        };

        img.src = imageUrl;
    });
}

async function renderImage() {

    var StoreUUN = searchInput.value
    var filtered = allStores.filter(item => item.uun.toLowerCase() == StoreUUN.toLowerCase())
    grocery = await getGrocery(StoreUUN)

    if (filtered.length != 1) {
        return
    }
    if (grocery === null) {
        return
    }
    groceryKeys = Object.keys(grocery).map(key => key.toLowerCase())

    const imagePath = '../json/stores/Lidl, Nuernberger Str., Altdorf bei Nuernberg.png';
    const markerColor = '#FF0000';
    const markerSize = 0.02;
    const markerFontSize = 18;

    getImageSize(imagePath)
        .then(({ width, height }) => {
            var shelves = []
            var points = []
        
            fetch('../json/Stores.json').then(response => {
                return response.json()
            }).then(data => {
                storeIndex = allStores.findIndex(item => item.uun.toLowerCase() == StoreUUN.toLowerCase())
                shoppingList.forEach(element => {
                    element = element.substring(2)
                    if (groceryKeys.includes(element.toLowerCase())) {
                        shelfNumber = grocery[element.toLowerCase()].shelf
                        if (!shelves.includes(shelfNumber)) {
                            shelves.push(shelfNumber)
                        }
                    }
                })
                console.log(data.Stores[storeIndex].shelves)
                shelves.forEach(element => {
                    var point = []
                    var xCoord = data.Stores[storeIndex].shelves[element].x / width
                    var yCoord = data.Stores[storeIndex].shelves[element].y / height
        
                    point.push(xCoord)
                    point.push(yCoord)
                    points.push(point)
                })
                addMarkerToImage(imagePath, points, markerColor, markerSize, markerFontSize);
            })
        })
        .catch(error => {
            console.error(error);
        });
}