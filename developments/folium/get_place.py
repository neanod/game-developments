import folium
import webbrowser

# location = eval('64.5401, 40.5433')
try:
	location = eval(input('>>>'))
except Exception as e:
	print("Invalid Input.")
	print(e)
	exit()

print(f"location: {location}")

place = folium.Map(location=location)
place.save('result.html')

webbrowser.open('result.html')
