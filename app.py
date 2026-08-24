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
# デッキ生成と手札配布
def generate_deck_and_deal():
  suits = ["♠", "♣", "♥", "♦"]
  suit_names = {
      "♠": "spade",
      "♣": "club",
      "♥": "heart",
      "♦": "diamond",
  }
  deck = []

  # 通常カードの生成 (4スート × 13数値 = 52枚)
  for suit in suits:
    for num in range(1, 14):
      # 画像ファイル名のマッピング例: images/spade_1.png など
      img_filename = f"images/{suit_names[suit]}_{num}.jpg"
      deck.append({
          "type": "normal",
          "suit": suit,
          "val": num,
          "id": f"{suit}{num}",
          "img": img_filename,
      })

  # 特殊カード（バグ・AI）の追加
  deck.append({
      "type": "bug",
      "suit": "🌟",
      "val": 0,
      "id": "BUG-01",
      "img": "images/bug_card.jpg",
  })
  deck.append({
      "type": "ai",
      "suit": "🤖",
      "val": 10,
      "id": "AI-01",
      "img": "images/ai_card.jpg",
  })

  random.shuffle(deck)

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
# プレイヤーターン：カード選択（サイバー戦場風ビジュアル）
st.subheader("🃏 サイバーデッキ（手札ターミナル）")
st.markdown(
    "戦場に展開されたプロトコルを選択し、敵メインフレームへハッキングコマンドを実行せよ。"
)

# 手札を横並びのカラムでリッチに表示して選ばせる
hand_cols = st.columns(len(st.session_state.player_hand))
selected_card_idx = None

# ラジオボタンの代わりに視覚的な選択肢として処理する場合のインデックス管理
# ここではシンプルにselectbox、またはカラム内のボタンで選択させる方式に拡張できます。
selected_card_idx = st.radio(
    "使用するカード（プロトコル）を選択:",
    options=range(len(st.session_state.player_hand)),
    format_func=lambda i: (
        f"[{st.session_state.player_hand[i]['id']}] "
        f"属性: {st.session_state.player_hand[i]['suit']} ｜ "
        f"演算値: {st.session_state.player_hand[i]['val']}"
    ),
    horizontal=True,
)

card = st.session_state.player_hand[selected_card_idx]

# 選択中カードのAI生成画像と詳細プレビュー表示
col_img, col_desc = st.columns([1, 2])
with col_img:
  # 画像ファイルが存在しない場合のフォールバックとしてエラーを防ぐため st.image を使用
  # ※ 実際に画像を用意したパス（例: "images/spade_1.png" など）を指定してください
  try:
    st.image(
        card["img"], width=140, caption=f"Protocol: {card['id']}"
    )  #
  except Exception:
    # 画像ファイルがまだ無い場合のプレースホルダー表示
    st.markdown(
        f"<div style='border: 2px dashed #00ffcc; padding: 30px; text-align: center; border-radius: 10px;'>"
        f"<h3>{card['id']}</h3><p>AI Card Art</p></div>",
        unsafe_allow_html=True,
    )

with col_desc:
  st.markdown("### 🎯 選択中プロトコルの解析データ")
  st.markdown(f"- **カードID:** `{card['id']}`")
  st.markdown(f"- **ベース数値:** `{card['val']}`")

  suit_effect_desc = {
      "♠": "🛡️ **ファイアウォール防御**：自陣のサーバー耐久値（HP）を強固にする。",
      "♣": "🦠 **ウイルス攻撃**：敵のメインフレームに直接ダメージを与える。",
      "♥": "💖 **システム修復**：破損したコードを修復しHPを回復する。",
      "♦": "💠 **資金獲得**：ハッキングに必要な暗号通貨（リソース）を拡張する。",
      "🌟": "⚠️ **バグカード**：何が起こるか分からない予測不能なハイリスク・ハイリターン効果。",
      "🤖": "🚀 **AIカード**：強力な攻守一体の専用演算処理を発動する。",
  }
  st.info(
      suit_effect_desc.get(
          card["suit"], "⚡ 特殊プロトコル：未知のシステム効果"
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
    st.toast("🤖 AI覚醒！ CPUに30ダメージ＆自陣HPが20回復！", icon="🚀")

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
