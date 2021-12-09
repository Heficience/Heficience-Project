import discord
from discord.ext import commands
from discord.utils import get
from github import Github


from data import add_people, get_people, remove_people, add_token, id_to_token, get_id


# -------------------------------------- Bot Informations -------------------------------------- #

client = commands.Bot(command_prefix="+", help_command=None)

# -------------------------------------- Lancement du bot informations -------------------------------------- #

@client.event
async def on_ready():
    print("Ready")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="+help"))

# -------------------------------------- Liste Administrateur ID -------------------------------------- #

admin_list = [454972825170870273, 471389909375123485, 708717385456156716, 744961307932885052, 774721383761575976]

# -------------------------------------- Shutdown Bot -------------------------------------- #

@client.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.bot.logout()

# -------------------------------------- Comment crée son token ! -------------------------------------- #

@client.command()
async def gentoken(ctx):
    member = ctx.author.id
    if member in get_people():
        await ctx.send("""
        
        > Pour crée ton token il faut te rediriger sur ce lien : https://github.com/
        > Tu vas devoir te rediriger sur ton profil puis allez dans **Settings**
        > Une fois de dans tu vas descendre en bas et aller dans **Developer settings**
        > Ensuite tu choisi **Personal access tokens**
        > Puis tu clicks sur le bouton **Generate new token**
        > Voilà tu as ton token ! Tu peux l'inscrire ainsi dans dans la liste !
        
        > ** Commandes ** => A FAIRE EN MP DU BOT
        >    
        > +token ***Ici le token***
        
        """)
    elif not member in get_people():
        await ctx.send("Tu n'as pas la permission !")

# -------------------------------------- Creation du repository sur github -------------------------------------- #

def create_project(n, id, private:bool = None):
    name_of_project = n
    user = Github(f"{id}").get_organization('Heficience')
    user.create_repo(name=name_of_project, private=private)

# -------------------------------------- Ajout de la permission pour poster sur github -------------------------------------- #

@client.command()
async def addgit(ctx, member:int = None):
    user = ctx.author.id
    if user in admin_list:
        if member == None:
            await ctx.send("Veuillez entrez un identifiants !")
        else:
            if add_people(member) == True:
                await ctx.send(f"L'utilisateur <@{member}> a **déjà** était ajouté !")
            else:
                add_people(member)
                await ctx.send(f"L'utilisateur <@{member}> a bien était ajouté !")
    elif not user in admin_list:
        await ctx.send("Tu n'as pas la permission !")


# -------------------------------------- Retirer la permission pour poster sur github -------------------------------------- #

@client.command()
async def removegit(ctx, member:int = None):
    user = ctx.author.id
    if user in admin_list:
        if member == None:
            await ctx.send("Veuillez entrez un identifiants !")
        else:
            if not member in get_people():
                await ctx.send(f"L'utilisateur <@{member}> n'est pas dans la liste !")
            else:
                remove_people(member)
                await ctx.send(f"L'utilisateur <@{member}> a bien était **retiré** !")

    elif not user in admin_list:
        await ctx.send("Tu n'as pas la permission !")

# -------------------------------------- Projets + Création channel sur le discord -------------------------------------- #

@client.command(pass_context=True)
@commands.has_permissions(manage_channels=True, manage_roles=True)
async def projects(ctx, id:str, name: str = None, private:bool = None):
    member = ctx.author.id
    identifiant = str(id)
    if member in get_people():
        if name == None:
            await ctx.send("Veuillez entrez un nom de project")
        else:
            if identifiant in get_id():
                id_token = id_to_token(identifiant)
                create_project(name, id_token, private)
                user = "heficience"
                await ctx.send(f"Succès dépôt crée ! https://www.github.com/{user}/{name}")
                guild = ctx.guild
                role = name
                autorize_role = await guild.create_role(name=role)
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    guild.me: discord.PermissionOverwrite(read_messages=True),
                    autorize_role: discord.PermissionOverwrite(read_messages=True)
                }
                await guild.create_text_channel(name, overwrites=overwrites,
                                                category=discord.utils.get(ctx.guild.categories, name='Project'))
                await ctx.author.add_roles(autorize_role)
                await ctx.send(f"Le channel **{name.lower()}** a bien était crée ! ")
            else:
                await ctx.send(f"Veuillez entrez un identifiant correcte")

    elif not member in get_people():
        await ctx.send("Tu n'as pas la permission !")

# -------------------------------------- Ajout token -------------------------------------- #

@client.command()
async def token(ctx, token = None):
    member = ctx.author.id
    if member in get_people():
        if token is None:
            await ctx.send("Veuillez entrez un token !")
        else:

            await ctx.send(f"Votre identifiants est donc => **{add_token(token)}**")
    elif not member in get_people():
        await ctx.send("Tu n'as pas la permission !")

# -------------------------------------- Regarder tout les utilisateurs -------------------------------------- #

@client.command()
async def user(ctx):
    message = "Heficence Members => \n"
    for ppl in get_people():
        message += f'> <@{str(ppl)}>' + '\n'

    await ctx.send(message)

# -------------------------------------- Help -------------------------------------- #

@client.command()
async def help(ctx):
    embed = discord.Embed(title="Help Commands",
                          description="=> +projects ID Nomdurepo True Ou False - Création d'un project automatiquement (Discord ( Salon ) + Github ( Repo )\n"
                                      "\n=> +gentoken - Explication pour génerer ton token !\n"
                                      "\n=> +token tontoken - Permet de mettre ton token dans la liste\n"
                                      "\n\n True = Depot privée | False = Depot public",
                          color=0xf1c40f)
    embed.set_thumbnail(url="https://imgur.com/d5JaaER.png")
    await ctx.send(embed=embed)


client.run("OTE2NzU2Mzk5MjM1Njg2NDAx.Yaux7g.OE12mKOFrJ07H3A7sKOfuCDpw5o")
