from flask import Flask, render_template, request, redirect
from classes import unit_classes
from equipment import Equipment
from arena import Arena
from unit import BaseUnit, PlayerUnit, PC_Unit

app = Flask(__name__)

heroes = {
    "player": BaseUnit,
    "enemy": BaseUnit
}

arena = Arena()
equipment = Equipment()


@app.route("/")
def menu_page():
    return render_template('index.html')


@app.route("/choose-hero/", methods=['POST', 'GET'])
def choose_hero():
    if request.method == 'GET':
        result = {
            'classes': unit_classes.keys(),
            'weapons': equipment.get_weapon_names(),
            'armors': equipment.get_armor_names()
        }
        return render_template('hero_choosing.html', result=result)

    elif request.method == 'POST':
        result = dict(request.form) # Получение данных из формы в виде словаря

        # Создание объекта PlayerUnit с данными о выбранном игроком имени и классе юнита, полученными из формы.
        heroes["player"] = PlayerUnit(name=result.get('name'), unit_class=unit_classes[result.get('unit_class')])
        # Выборы из словаря equipment по названию, полученному из формы.
        weapon = equipment.get_weapon(result.get('weapon'))
        armor = equipment.get_armor(result.get('armor'))
        # Экипировка выбранного оружия на созданного игрока.
        heroes['player'].equip_weapon(weapon)
        heroes['player'].equip_armor(armor)
        return redirect('/choose-enemy/')


@app.route("/choose-enemy/", methods=['POST', 'GET'])
def choose_enemy():
    if request.method == 'GET':
        result = {
            'classes': unit_classes.keys(),
            'weapons': equipment.get_weapon_names(),
            'armors': equipment.get_armor_names()
        }
        return render_template('hero_choosing.html', result=result)

    elif request.method == 'POST':
        result = dict(request.form) # Получение данных из формы в виде словаря

        # Создание объекта PlayerUnit с данными о выбранном игроком имени и классе юнита, полученными из формы.
        heroes["enemy"] = PC_Unit(name=result.get('name'), unit_class=unit_classes[result.get('unit_class')])
        # Выборы из словаря equipment по названию, полученному из формы.
        weapon = equipment.get_weapon(result.get('weapon'))
        armor = equipment.get_armor(result.get('armor'))
        # Экипировка выбранного оружия на созданного игрока.
        heroes['enemy'].equip_weapon(weapon)
        heroes['enemy'].equip_armor(armor)
        return redirect('/fight/') # перенаправить пользователя на другую страницу



@app.route("/fight/")
def start_fight():
    # выполняем функцию start_game экземпляра класса арена и передаем ему необходимые аргументы
    arena.start_game(player=heroes.get('player') , enemy=heroes.get('enemy'))
    return render_template('fight.html', heroes=heroes)


@app.route("/fight/hit")
def hit():
    result, battle_result = '', ''
    if arena.game_is_running:
       result = arena.player_hit()
    if arena._check_players_hp():
        battle_result = arena._end_game()
    else:
        turn_result = arena.next_turn()
        if turn_result:
            result += turn_result
    return render_template('fight.html', heroes=heroes, result=result, battle_result=battle_result)


@app.route("/fight/use-skill")
def use_skill():
    result, battle_result = '', ''
    if arena.game_is_running:
       result = arena.player_use_skill()
    if arena._check_players_hp():
        battle_result = arena._end_game()
    if result:
        result += arena.next_turn()
    elif not result:
        result = 'Умение уже использовано'
    return render_template('fight.html', heroes=heroes, result=result, battle_result=battle_result)


@app.route("/fight/pass-turn")
def pass_turn():
    if arena.game_is_running:
       result, battle_result = arena.next_turn(), ''
    else:
        result, battle_result = '', arena._end_game()
    return render_template('fight.html', heroes=heroes, result=result, battle_result=battle_result)


@app.route("/fight/end-fight")
def end_fight():
    arena.battle_result = ''
    return redirect('/')


if __name__ == "__main__":
    app.run()
