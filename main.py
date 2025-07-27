#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テキストアドベンチャーゲーム: 魔法の森の冒険
"""

import random
import time
import sys

class Player:
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.max_hp = 100
        self.attack = 20
        self.gold = 50
        self.inventory = []
        self.level = 1
        self.experience = 0
    
    def is_alive(self):
        return self.hp > 0
    
    def take_damage(self, damage):
        self.hp = max(0, self.hp - damage)
    
    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)
    
    def gain_experience(self, exp):
        self.experience += exp
        if self.experience >= self.level * 100:
            self.level_up()
    
    def level_up(self):
        self.level += 1
        self.max_hp += 20
        self.hp = self.max_hp
        self.attack += 5
        print(f"\n🎉 レベルアップ！レベル{self.level}になりました！")
        print(f"HP: {self.max_hp}, 攻撃力: {self.attack}")

class Enemy:
    def __init__(self, name, hp, attack, gold_reward, exp_reward):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.gold_reward = gold_reward
        self.exp_reward = exp_reward
    
    def is_alive(self):
        return self.hp > 0
    
    def take_damage(self, damage):
        self.hp = max(0, self.hp - damage)

class Game:
    def __init__(self):
        self.player = None
        self.enemies = {
            "スライム": Enemy("スライム", 30, 10, 20, 25),
            "ゴブリン": Enemy("ゴブリン", 50, 15, 35, 40),
            "オーク": Enemy("オーク", 80, 25, 60, 70),
            "ドラゴン": Enemy("ドラゴン", 150, 40, 200, 150)
        }
    
    def clear_screen(self):
        """画面をクリアする（クロスプラットフォーム対応）"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def typewriter_print(self, text, delay=0.03):
        """タイプライター効果でテキストを表示"""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
    
    def show_status(self):
        """プレイヤーのステータスを表示"""
        print(f"\n{'='*50}")
        print(f"🧙 {self.player.name} | レベル: {self.player.level}")
        print(f"❤️  HP: {self.player.hp}/{self.player.max_hp}")
        print(f"⚔️  攻撃力: {self.player.attack}")
        print(f"💰 ゴールド: {self.player.gold}")
        print(f"✨ 経験値: {self.player.experience}")
        if self.player.inventory:
            print(f"🎒 アイテム: {', '.join(self.player.inventory)}")
        print(f"{'='*50}")
    
    def get_choice(self, prompt, choices):
        """選択肢を表示してユーザーの入力を取得"""
        while True:
            print(f"\n{prompt}")
            for i, choice in enumerate(choices, 1):
                print(f"{i}. {choice}")
            
            try:
                choice = int(input("\n選択してください (数字): "))
                if 1 <= choice <= len(choices):
                    return choice - 1
                else:
                    print("⚠️  無効な選択です。もう一度入力してください。")
            except ValueError:
                print("⚠️  数字を入力してください。")
    
    def battle(self, enemy):
        """戦闘システム"""
        print(f"\n⚔️  {enemy.name}が現れた！")
        print(f"{enemy.name}: HP {enemy.hp}, 攻撃力 {enemy.attack}")
        
        while enemy.is_alive() and self.player.is_alive():
            action = self.get_choice(
                "どうしますか？",
                ["攻撃する", "逃げる", "ポーションを使う"]
            )
            
            if action == 0:  # 攻撃
                damage = random.randint(self.player.attack - 5, self.player.attack + 5)
                enemy.take_damage(damage)
                print(f"\n💥 {enemy.name}に{damage}ダメージを与えた！")
                
                if enemy.is_alive():
                    print(f"{enemy.name}: HP {enemy.hp}/{enemy.max_hp}")
                    
                    # 敵の攻撃
                    enemy_damage = random.randint(enemy.attack - 3, enemy.attack + 3)
                    self.player.take_damage(enemy_damage)
                    print(f"💔 {enemy.name}の攻撃！{enemy_damage}ダメージを受けた！")
                    print(f"あなたのHP: {self.player.hp}/{self.player.max_hp}")
                
            elif action == 1:  # 逃げる
                if random.random() < 0.7:
                    print("\n💨 うまく逃げることができた！")
                    return False
                else:
                    print("\n❌ 逃げられなかった！")
                    enemy_damage = random.randint(enemy.attack - 3, enemy.attack + 3)
                    self.player.take_damage(enemy_damage)
                    print(f"💔 {enemy.name}の攻撃！{enemy_damage}ダメージを受けた！")
            
            elif action == 2:  # ポーション
                if "ヒーリングポーション" in self.player.inventory:
                    self.player.inventory.remove("ヒーリングポーション")
                    heal_amount = random.randint(30, 50)
                    self.player.heal(heal_amount)
                    print(f"\n🧪 ヒーリングポーションを使った！HP が {heal_amount} 回復した！")
                    print(f"現在のHP: {self.player.hp}/{self.player.max_hp}")
                else:
                    print("\n❌ ポーションを持っていません！")
                    continue
        
        if enemy.is_alive() and not self.player.is_alive():
            return False
        elif not enemy.is_alive():
            print(f"\n🎉 {enemy.name}を倒した！")
            self.player.gold += enemy.gold_reward
            self.player.gain_experience(enemy.exp_reward)
            print(f"💰 {enemy.gold_reward}ゴールドを獲得！")
            print(f"✨ {enemy.exp_reward}経験値を獲得！")
            
            # アイテムドロップのチャンス
            if random.random() < 0.3:
                item = "ヒーリングポーション"
                self.player.inventory.append(item)
                print(f"🎁 {item}を見つけた！")
            
            return True
    
    def shop(self):
        """ショップシステム"""
        print("\n🏪 ようこそ、魔法のお店へ！")
        
        items = {
            "ヒーリングポーション": 30,
            "攻撃力アップの薬": 100,
            "最大HP増加の薬": 150
        }
        
        while True:
            print(f"\n💰 所持金: {self.player.gold}ゴールド")
            print("\n商品一覧:")
            choices = []
            for item, price in items.items():
                print(f"- {item}: {price}ゴールド")
                choices.append(f"{item}を買う ({price}G)")
            choices.append("店を出る")
            
            choice = self.get_choice("何を買いますか？", choices)
            
            if choice == len(choices) - 1:  # 店を出る
                print("\n👋 またのお越しをお待ちしております！")
                break
            
            item_name = list(items.keys())[choice]
            price = items[item_name]
            
            if self.player.gold >= price:
                self.player.gold -= price
                
                if item_name == "ヒーリングポーション":
                    self.player.inventory.append(item_name)
                    print(f"\n✅ {item_name}を購入しました！")
                elif item_name == "攻撃力アップの薬":
                    self.player.attack += 10
                    print(f"\n✅ 攻撃力が10上がりました！現在の攻撃力: {self.player.attack}")
                elif item_name == "最大HP増加の薬":
                    self.player.max_hp += 30
                    self.player.hp += 30
                    print(f"\n✅ 最大HPが30上がりました！現在のHP: {self.player.hp}/{self.player.max_hp}")
            else:
                print(f"\n❌ ゴールドが足りません！あと{price - self.player.gold}ゴールド必要です。")
    
    def forest_adventure(self):
        """森での冒険"""
        events = [
            "treasure", "enemy", "nothing", "shop", "healing_spring"
        ]
        
        event = random.choice(events)
        
        if event == "treasure":
            gold_found = random.randint(20, 80)
            self.player.gold += gold_found
            print(f"\n💎 宝箱を発見！{gold_found}ゴールドを見つけた！")
            
        elif event == "enemy":
            enemy_name = random.choice(list(self.enemies.keys()))
            enemy = Enemy(**self.enemies[enemy_name].__dict__)
            return self.battle(enemy)
            
        elif event == "nothing":
            messages = [
                "静かな森を歩いている...",
                "美しい花を見つけた。",
                "小鳥のさえずりが聞こえる。",
                "きれいな小川が流れている。"
            ]
            print(f"\n🌲 {random.choice(messages)}")
            
        elif event == "shop":
            print("\n🏪 森の奥で旅商人に出会った！")
            self.shop()
            
        elif event == "healing_spring":
            heal_amount = random.randint(20, 40)
            self.player.heal(heal_amount)
            print(f"\n⛲ 癒しの泉を発見！HPが{heal_amount}回復した！")
            print(f"現在のHP: {self.player.hp}/{self.player.max_hp}")
        
        return True
    
    def start_game(self):
        """ゲーム開始"""
        self.clear_screen()
        print("🌟" * 30)
        self.typewriter_print("✨ 魔法の森の冒険へようこそ！ ✨", 0.05)
        print("🌟" * 30)
        
        name = input("\n🧙 あなたの名前を教えてください: ")
        self.player = Player(name)
        
        print(f"\nようこそ、{name}さん！")
        print("あなたは魔法の森で冒険を始めます。")
        print("モンスターを倒し、宝物を集めて、強くなりましょう！")
        
        input("\nエンターキーを押して冒険を始める...")
        
        # メインゲームループ
        while self.player.is_alive():
            self.show_status()
            
            action = self.get_choice(
                "何をしますか？",
                ["森を探索する", "ショップに行く", "ステータスを確認", "ゲームを終了"]
            )
            
            if action == 0:  # 森を探索
                print("\n🌲 森の奥へ向かいます...")
                time.sleep(1)
                
                if not self.forest_adventure():
                    print("\n💀 あなたは力尽きました...")
                    break
                    
            elif action == 1:  # ショップ
                self.shop()
                
            elif action == 2:  # ステータス確認
                continue
                
            elif action == 3:  # ゲーム終了
                print(f"\n👋 冒険お疲れさまでした、{self.player.name}さん！")
                print(f"最終レベル: {self.player.level}")
                print(f"最終ゴールド: {self.player.gold}")
                break
            
            # 継続確認
            if action == 0:
                continue_game = self.get_choice(
                    "冒険を続けますか？",
                    ["はい", "いいえ"]
                )
                if continue_game == 1:
                    break
        
        if not self.player.is_alive():
            print("\n💀 ゲームオーバー")
            print("また挑戦してください！")
        
        print("\nゲームを終了します。ありがとうございました！")

def main():
    """メイン関数"""
    try:
        game = Game()
        game.start_game()
    except KeyboardInterrupt:
        print("\n\nゲームを中断しました。")
    except Exception as e:
        print(f"\nエラーが発生しました: {e}")
        print("ゲームを再起動してください。")

if __name__ == "__main__":
    main()
