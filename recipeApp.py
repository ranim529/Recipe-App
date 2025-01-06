from io import BytesIO
from PIL import Image, ImageTk
import requests
import tkinter as tk
import webbrowser

WINDOW_TITLE = "Recipe App"
RECIPE_IMAGE_WIDTH = 300
RECIPE_IMAGE_HEIGHT = 300
SPOONACULAR_API_KEY = "551362774526425f8bfac59f760cc504" #here you put your own key
SPOONACULAR_URL = "https://api.spoonacular.com/recipes/complexSearch"  # we use spoonacular site web that contain the recipes
SPOONACULAR_RECIPE_URL = "https://api.spoonacular.com/recipes/{}/information"

class RecipeApp(object):

    def __init__(self):  
        self.window = tk.Tk()

        # Auto resize geometry
        self.window.geometry("")
        self.window.configure(bg="#FF00FF")
        self.window.title(WINDOW_TITLE)

        self.search_label = tk.Label(self.window, text="Search Recipe", bg="#6b92ed")
        self.search_label.grid(column=0, row=0, padx=5)

        self.search_entry = tk.Entry(master=self.window, width=40)
        self.search_entry.grid(column=1, row=0, padx=5, pady=10)

        self.search_button = tk.Button(self.window, text="search", highlightbackground="#ffffff",
                                       command=self.__run_search_query)
        self.search_button.grid(column=2, row=0, padx=5)

    def __run_search_query(self):
        query = self.search_entry.get()
        recipe = self.__get_recipe(query)

        if recipe:
            recipe_image = recipe["image"]
            recipe_url = f"https://spoonacular.com/recipes/{recipe['title'].replace(' ', '-')}-{recipe['id']}"
        else:
            # Recipe not found
            recipe_image = "https://www.mageworx.com/blog/wp-content/uploads/2012/06/Page-Not-Found-13.jpg"
            recipe_url = ""

        self.__show_image(recipe_image)
        self.__get_ingredients(recipe)

        def __open_link():
            webbrowser.open(recipe_url)

        self.recipe_button = tk.Button(self.window, text="recipe link", highlightbackground="#ea86b6",
                                       command=__open_link)
        self.recipe_button.grid(column=1, row=7, pady=0)

    def __get_recipe(self, query):
        params = {
            "query": query,
            "apiKey": SPOONACULAR_API_KEY,
            "number": 1  # Return only one recipe for simplicity
        }

        response = requests.get(SPOONACULAR_URL, params=params)
        data = response.json()

        if data["results"]:
            recipe_id = data["results"][0]["id"]
            # Get detailed recipe info
            return self.__get_recipe_details(recipe_id)
        return None

    def __get_recipe_details(self, recipe_id):
        params = {
            "apiKey": SPOONACULAR_API_KEY
        }

        response = requests.get(SPOONACULAR_RECIPE_URL.format(recipe_id), params=params)
        data = response.json()

        if data:
            return data  # Returns detailed recipe data including ingredients
        return None

    def __show_image(self, image_url):
        try:
            response = requests.get(image_url)
            img = Image.open(BytesIO(response.content))
            img = img.resize((RECIPE_IMAGE_WIDTH, RECIPE_IMAGE_HEIGHT))
            image = ImageTk.PhotoImage(img)

            holder = tk.Label(self.window, image=image)
            holder.photo = image
            holder.grid(column=1, row=6, pady=10)
        except Exception as e:
            print(f"Error fetching image: {e}")

    def __get_ingredients(self, recipe):
        ingredients = tk.Text(master=self.window, height=15, width=50, bg="#ffdada")
        ingredients.grid(column=1, row=4, pady=10)
        ingredients.delete("1.0", tk.END)

        if recipe is None:
            ingredients.insert(tk.END, "No Recipe found for search criteria")
            return

        ingredients.insert(tk.END, "\n" + recipe["title"] + "\n")
        for ingredient in recipe.get("extendedIngredients", []):
            ingredients.insert(tk.END, "\n- " + ingredient["name"])

    def run_app(self):
        self.window.mainloop()


if __name__ == "__main__":
    recipe_app = RecipeApp()
    recipe_app.run_app()
