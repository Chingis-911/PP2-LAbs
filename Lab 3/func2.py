movies = [
{
"name": "Usual Suspects", 
"imdb": 7.0,
"category": "Thriller"
},
{
"name": "Hitman",
"imdb": 6.3,
"category": "Action"
},
{
"name": "Dark Knight",
"imdb": 9.0,
"category": "Adventure"
},
{
"name": "The Help",
"imdb": 8.0,
"category": "Drama"
},
{
"name": "The Choice",
"imdb": 6.2,
"category": "Romance"
},
{
"name": "Colonia",
"imdb": 7.4,
"category": "Romance"
},
{
"name": "Love",
"imdb": 6.0,
"category": "Romance"
},
{
"name": "Bride Wars",
"imdb": 5.4,
"category": "Romance"
},
{
"name": "AlphaJet",
"imdb": 3.2,
"category": "War"
},
{
"name": "Ringing Crime",
"imdb": 4.0,
"category": "Crime"
},
{
"name": "Joking muck",
"imdb": 7.2,
"category": "Comedy"
},
{
"name": "What is the name",
"imdb": 9.2,
"category": "Suspense"
},
{
"name": "Detective",
"imdb": 7.0,
"category": "Suspense"
},
{
"name": "Exam",
"imdb": 4.2,
"category": "Thriller"
},
{
"name": "We Two",
"imdb": 7.2,
"category": "Romance"
}
]
 
def rank(n):
    for movie in movies: 
        if movie["name"] == n:  
            return movie["imdb"] > 5.5  
    return False  

list1 = []
def subl():
   return [movie["name"] for movie in movies if movie["imdb"] > 5.5]

x = input("Enter movie name: ")
if rank(x):
    print("True")
else:
   print("No such movie!")    

list1 = subl()
print(list1)

z = input("Enter the category: ")
def categ(m):
 return [movie["name"] for movie in movies if movie["category"] == m]

list2 = []
list2 = categ(z)
print(list2)

def aver(movie_list):
    tot = 0
    count = 0

    for movie in movies:
        if movie["name"] in movie_list:
            tot += movie["imdb"]
            count += 1

    if count == 0:  
        return "No matching movies found."

    return tot / count  



list3 = input("Enter some movies: ").split(", ") 

print("Average IMDb rating:", aver(list3))


def aver1(l):
    total = 0
    count1 = 0

    for movie in movies:
        if movie["category"] == l:
            total += movie["imdb"]
            count1 += 1

    if count1 == 0:  
        return "No matching movies found."

    return total / count1  

l = input("Enter the category: ")



print("Average IMDb rating:", aver1(l))