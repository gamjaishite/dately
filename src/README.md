# IF2250-2023-K02-12-Dately

## 🤖 How to Develop?

1. Clone this repository
2. Change directory to the **src** folder of the repository and create python virtual environment using the following commands:

   ```bash
   # windows
   python -m virtualenv .

   # macos
   python3 -m venv .
   ```

3. Then activate it:

   ```bash
   # windows
   ./Scripts/activate

   # macos
   source ./bin/activate
   ```

4. Finally, install all the packages using:

   ```bash
   pip install -r requirements.txt
   ```

5. Enjoy hacking!⚡🙌

## Testing

```bash
pytest --ignore=Lib --ignore=Include --ignore=Script
```

## ⚡⚡ Tips and Resources

- Compile the app using `flet -r main.py --assets assets` **only** for creating ui, **not for doing action that related to database**. If want to develop the backend related to database run the app using the normal command like `py main.py`
- Change **line 45** based on bagian masing-masing :v
- ORM using [SQLModel](https://sqlmodel.tiangolo.com/)
- Input validation using [Pydantic](https://docs.pydantic.dev/)
- [Official Docs](https://flet.dev/docs/)
- Icons are from [here](https://fontawesome.com/search?q=t%20shirt&o=r&m=free)
- Remember to always using the virtual environment
