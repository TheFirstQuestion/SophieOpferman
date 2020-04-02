from Work import *
from github import Github
import requests

###### Constants ######
DB_NAME = "SophieOpferman.db"
README_DELIMITER = "_____"
#######################

entries = [
    ["Big Brother is in the Details", "https://docs.google.com/document/d/1ffgf8IvBfSL4LJgKirGc0Slz2itNIW96QObapagYic0/edit?usp=sharing", "A discussion of the inherent dangers of technology and possible solutions.", "writing", "nonfiction", "complete"],
    ["Arduino Crash Course", "https://docs.google.com/document/d/1I4VCLLz57vo2Q3o-Cn9WBOVAiZtwCCA18Kl0zF1UBi8/edit?usp=sharing", "An introduction to Arduino for people with no programming experience and no circuitry experience.", "writing", "nonfiction", "complete"],
    ["The Morning After", "https://docs.google.com/document/d/1snuhEsLWgzR8zN18UhaCV9wk6UqX7GuSOEiVzVfH0Ho/edit?usp=sharing", "Taylor and Vanessa are best friends. Or maybe more?<br>Concurrent with <em>The Night Before</em>, can be read in either order.", "writing", "original", "short story"],
    ["The Night Before", "https://docs.google.com/document/d/11BQcNRT0Mnpa_nU7iyGPRMKMn4S-Nft16n4uwrGp8rE/edit?usp=sharing", "Taylor and Vanessa are best friends. Or maybe more?<br>Concurrent with <em>The Morning After</em>, can be read in either order.", "writing", "original", "short story"],
    ["Lost Boy", "https://musescore.com/user/6291301/scores/5127292", "An original arrangement of 'Lost Boy' by Ruth B.", "music", "derivative", ""],
    ["Titanium / Bulletproof / Stronger", "https://musescore.com/user/6291301/scores/5127224", "An original mashup of 'Titanium' by David Guetta, 'Bulletproof' by La Roux, and 'Stronger (What Doesn't Kill You)' by Kelly Clarkson.", "music", "derivative", ""],
    ["Sparks Fly", "https://musescore.com/user/6291301/scores/5654895", "An original song, for a typical pop band.", "music", "original", ""],
    ["Katherine in F# Minor", "https://musescore.com/user/6291301/scores/5655157", "An original song, for classical piano.", "music", "original", ""],
    ["Later", "https://docs.google.com/document/d/1I9OSV-UDRFJwqD1DbXdPqbalJsYAB6EMSsU7r5aKqss/edit?usp=sharing", "Sequel to <em>The Morning After/The Night Before</em>.", "writing", "original", "short story"],
    ["Recruited", "https://docs.google.com/document/d/1yZyJxQTFteSM5ZF4UbMnLSzJxBmlDVTokiac2XBiJbk/edit?usp=sharing", "An awkward college freshman is recruited by a mesmerizing junior for a revenge scheme which seems, frankly, to have a bit of an ulterior motive.", "writing", "original", "short story"],
    ["The Magickers", "https://docs.google.com/document/d/1peacNRWUUkgW4eIOthtn1VC7HoiW2nt-hQGTWgsYWBg/edit?usp=sharing", "In world where magic is limited by colors, two factions are in constant conflict on their search for The One, an omnipotent Magicker who will save the world from destruction. Octavio and Callum Florez are recruited by opposing forces, but they don't want to fight. All they want is to get away from the death and destruction that fills their lives.", "writing", "original", "short story"],
    ["Kiss the Girl", "https://docs.google.com/document/d/1qDjy0p0ovOiHHw22my62OJlfzvsT71uE2DHFh7VkL3c/edit?usp=sharing", "An imagining of a first kiss between a couple with dreams of the future.", "writing", "original", "short story"],
    ["February 10", "https://docs.google.com/document/d/1HBbE2yyce5GV_Q-6LzPy_lSD7MPAmdZSKgUyIQR-8lQ/edit?usp=sharing", "Martha is not a Valentine's Day kind of person. Sure, she's romantic, but she just has more important things to focus on. But a mysterious secret admirer doesn't care.", "writing", "original","short story"],
    ["The Ring", "https://docs.google.com/document/d/1NaBsfCKYw6B4rNIONJQikByKXNt1QxAirYeJ6DK2440/edit?usp=sharing", "Based on the TV show <em>Once Upon a Time</em>. Amelia Lancaster has been Emma Swan's best friend and partner in crime for years. She accompanies Emma to Storybrooke, where she finds herself drawn to the magic of the town and determined to protect the people thereof.", "writing", "derivative", "scene"],
    ["The Red Pyramid", "https://docs.google.com/document/d/1z3ZeG_xuVpxiiU34AWMVDUBtV1qQNb9BRAb6e25U4ko/edit?usp=sharing", "Based on Rick Riordan's novel of the same name. The story follows the Kane siblings Carter, Katherine, and Sadie as they discover they are descended from both the pharaohs and magicians of ancient Egypt. As a result, they are able to both host gods and wield magic.", "writing", "derivative", "incomplete"],
    ["The Throne of Fire", "https://docs.google.com/document/d/1z6l_CT8JDPBTSrHP1Gdz1a624HTzPxwJqMIAKTk8Vdo/edit?usp=sharing", "Sequel to <em>The Red Pyramid</em>. The Kane siblings continue on their mission to defeat Apophis, the Serpent of Chaos. But first, they must awaken Ra, king of the gods.", "writing", "derivative", "incomplete"]
]


if __name__ == "__main__":
    engine = create_engine('sqlite:///' + DB_NAME)
    session = sessionmaker()
    session.configure(bind=engine)
    Base.metadata.create_all(engine)
    s=session()

    for i in entries:
        print(i[0])
        s.add(Work(name=i[0], link=i[1], description=i[2], category=i[3], subcategory=i[4], status=i[5], demoLink=None))

    s.commit()

    with open('github-access-token.txt') as f:
        token = f.readlines()[0][:-1]
    g = Github(token)

    for repo in g.get_user().get_repos():
        topics = repo.get_topics()
        if "sgo-onsite" in topics:
            print(repo.name)
            status = None
            link = "https://raw.githubusercontent.com/TheFirstQuestion/" + repo.name + "/master/README.md"
            f = requests.get(link)
            readme = f.text
            pos1 = readme.find(README_DELIMITER)
            pos2 = readme.find(README_DELIMITER, pos1+len(README_DELIMITER))
            if pos1 < pos2:
                onsite, status = readme[pos1+len(README_DELIMITER):pos2].split(",")
                status = status.strip()

            s.add(Work(name=repo.name, link=repo.html_url, description=repo.description, category="programming", status=status, updated=repo.pushed_at, demoLink=repo.homepage))

    s.commit()
    s.close()
