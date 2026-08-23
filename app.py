import random
import streamlit as st

# ページ設定
st.set_page_config(
    page_title="スート・コード：ネットワーク", page_icon="💻", layout="wide"
)


# ゲーム状態の初期化
def init_game():
  st.session_state.player_hp = 100
  st.session_state.cpu_hp = 100
  st.session_state.player_credits = 10
  st.session_state.cpu_credits = 10
  st.session_state.turn = 1
  st.session_state.game_over = False
  st.session_state.winner = None
  generate_deck_and_deal()


# デッキ生成と手札配布
def generate_deck_and_deal():
  suits = ["♠", "♣", "♥", "♦"]
  deck = []

  # 通常カードの生成 (数字 1〜13)
  for suit in suits:
    for num in range(1, 14):
      deck.append({"type": "normal", "suit": suit, "val": num, "id": f"{suit}{num}"})

  # 特殊カード（バグ・AI）の追加
  deck.append({"type": "bug", "suit": "🌟", "val": 0, "id": "BUG-01"})
  deck.append({"type": "ai", "suit": "🤖", "val": 10, "id": "AI-01"})

  random.shuffle(deck)

  # プレイヤーとCPUに手札を配る (5枚ずつ)
  st.session_state.player_hand = [deck.pop() for _ in range(5)]
  st.session_state.cpu_hand = [deck.pop() for _ in range(5)]
  st.session_state.deck = deck


if "player_hp" not in st.session_state:
  init_game()

# タイトル
st.title("💻 スート・コード：ネットワーク")
st.markdown(
    "**サイバーパンク・ハッキングバトル — カードの数字とスートの特性を駆使して敵のメインフレームを制圧せよ！"
)

# ステータス表示
col1, col2, col3 = st.columns(3)
with col1:
  st.metric(
      label="プレイヤー サーバー耐久 (HP)",
      value=f"{st.session_state.player_hp} / 100",
  )
  st.metric(
      label="プレイヤー資金", value=f"{st.session_state.player_credits} ⚡"
  )
with col2:
  st.markdown(f"<h3 style='text-align: center;'>TURN {st.session_state.turn}</h3>", unsafe_allow_html=True)
with col3:
  st.metric(
      label="CPU サーバー耐久 (HP)", value=f"{st.session_state.cpu_hp} / 100"
  )
  st.metric(label="CPU資金", value=f"{st.session_state.cpu_credits} ⚡")

st.divider()

# 勝敗判定
if st.session_state.player_hp <= 0 or st.session_state.cpu_hp <= 0:
  st.session_state.game_over = True
  if st.session_state.player_hp <= 0:
    st.session_state.winner = "CPU"
  else:
    st.session_state.winner = "プレイヤー"

if st.session_state.game_over:
  if st.session_state.winner == "プレイヤー":
    st.balloons()
    st.success("🎉 ハッキング成功！敵のネットワークを制圧しました！")
  else:
    st.error("💥 ハッキング失敗… システムがロックアウトされました。")

  if st.button("🔄 システム再起動 (リトライ)"):
    init_game()
    st.rerun()
  st.stop()


# プレイヤーターン：カード選択
st.subheader("🃏 あなたの手札 (カードを選択してアクション)")
selected_card_idx = st.radio(
    "使用するカードを選んでください:",
    options=range(len(st.session_state.player_hand)),
    format_func=lambda i: f"[{st.session_state.player_hand[i]['id']}] (値: {st.session_state.player_hand[i]['val']})",
)

card = st.session_state.player_hand[selected_card_idx]

# AI生成画像のプレースホルダー表示用（必要に応じてURLやローカルパスに変更可能）
# 例: st.image("path/to/ai_character.png", width=150)

st.info(
    f"選択中カード: ** ｜ スート特性: "
    + (
        "♠ 防御 (ファイアウォール)"
        if card["suit"] == "♠"
        else (
            "♣ ウイルス攻撃"
            if card["suit"] == "♣"
            else (
                "♥ システム修復"
                if card["suit"] == "♥"
                else (
                    "♦ 資金獲得"
                    if card["suit"] == "♦"
                    else "⚡ 特殊効果 (バグ/AI)"
                )
            )
        )
    )
)

if st.button("🚀 カードを実行してハッキングをしかける", type="primary"):
  # プレイヤーのアクション処理
  damage_dealt = 0
  defense_gained = 0
  heal_gained = 0
  credit_gained = 0

  if card["type"] == "normal":
    if card["suit"] == "♣":  # ウイルス攻撃
      damage_dealt = card["val"] * 2
      st.session_state.cpu_hp = max(0, st.session_state.cpu_hp - damage_dealt)
      st.toast(
          f"ウイルス攻撃！ CPUに {damage_dealt} のダメージを与えました。",
          icon="🦠",
      )
    elif card["suit"] == "♠":  # ファイアウォール防御
      defense_gained = card["val"] * 2
      st.session_state.player_hp = min(
          100, st.session_state.player_hp + defense_gained
      )
      st.toast(f"システムを強化！ HPが {defense_gained} 回復しました。", icon="🛡️")
    elif card["suit"] == "♥":  # システム修復
      heal_gained = card["val"] * 1.5
      st.session_state.player_hp = min(
          100, st.session_state.player_hp + int(heal_gained)
      )
      st.toast(f"修復完了！ HPが {int(heal_gained)} 回復しました。", icon="💖")
    elif card["suit"] == "♦":  # 資金獲得
      credit_gained = card["val"]
      st.session_state.player_credits += credit_gained
      st.toast(f"暗号通貨を獲得！ +{credit_gained} ⚡", icon="💠")

  elif card["type"] == "bug":  # バグカード（ランダム効果）
    effect_type = random.choice(["self_damage", "big_attack", "credit_boost"])
    if effect_type == "self_damage":
      st.session_state.player_hp -= 10
      st.toast(
          "⚠️ バグ発生！ 自分のシステムが暴走し、10ダメージを受けました。",
          icon="💥",
      )
    elif effect_type == "big_attack":
      st.session_state.cpu_hp = max(0, st.session_state.cpu_hp - 25)
      st.toast("⚡ バグ・クラッシュ！ CPUに25の大ダメージを与えた！", icon="🔥")
    else:
      st.session_state.player_credits += 10
      st.toast("💰 不正アクセス成功！ 資金が10増加しました。", icon="💎")

  elif card["type"] == "ai":  # AIカード（強力な全体効果）
    st.session_state.cpu_hp = max(0, st.session_state.cpu_hp - 30)
    st.session_state.player_hp = min(100, st.session_state.player_hp + 20)
    .toast("🤖 AI覚醒！ CPUに30ダメージ＆自陣HPが20回復！", icon="🚀")

  # 手札から使用したカードを削除し、新しいカードを1枚補充
  st.session_state.player_hand.pop(selected_card_idx)
  if st.session_state.deck:
    st.session_state.player_hand.append(st.session_state.deck.pop())

  # --- CPUのターン処理 ---
  if st.session_state.cpu_hp > 0 and st.session_state.cpu_hand:
    cpu_card = st.session_state.cpu_hand.pop(
        random.randint(0, len(st.session_state.cpu_hand) - 1)
    )
    if cpu_card["type"] == "normal":
      if cpu_card["suit"] == "♣":
        cpu_dmg = cpu_card["val"] * 2
        st.session_state.player_hp = max(
            0, st.session_state.player_hp - cpu_dmg
        )
        st.toast(
            f"敵(CPU)の反撃！ ウイルス攻撃で {cpu_dmg} のダメージを受けた！",
            icon="🚨",
        )
      else:
        cpu_heal = cpu_card["val"]
        st.session_state.cpu_hp = min(100, st.session_state.cpu_hp + cpu_heal)
        st.toast(f"敵(CPU)がシステムを修復しました。", icon="🔧")
    else:
      st.session_state.player_hp = max(0, st.session_state.player_hp - 15)
      st.toast("敵(CPU)が特殊AIコマンドを発動！ 15ダメージ！", icon="⚠️")

    if st.session_state.deck:
      st.session_state.cpu_hand.append(st.session_state.deck.pop())

  st.session_state.turn += 1
  st.rerun()
