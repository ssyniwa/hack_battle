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


# デッキ生成と手札配布（捨て札・山札システムの導入）
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

  st.session_state.deck = deck
  st.session_state.discard_pile = []  # 捨て札置き場
  st.session_state.player_hand = [st.session_state.deck.pop() for _ in range(5)]
  st.session_state.cpu_hand = [st.session_state.cpu_hand.pop() if 'cpu_hand' in st.session_state and st.session_state.cpu_hand else st.session_state.deck.pop() for _ in range(5)] if 'cpu_hand' not in st.session_state else [st.session_state.deck.pop() for _ in range(5)]

# カード補充関数（山札が枯渇したら捨て札をシャッフルして再利用）
def draw_card_for_player():
  if not st.session_state.deck:
    if st.session_state.discard_pile:
      st.session_state.deck = st.session_state.discard_pile
      st.session_state.discard_pile = []
      random.shuffle(st.session_state.deck)
      st.toast("🔄 山札が尽きたため、捨て札を再シャッフルしました！", icon="♻️")
    else:
      return None  # 完全になくなったら引けない
  return st.session_state.deck.pop()

def draw_card_for_cpu():
  if not st.session_state.deck:
    if st.session_state.discard_pile:
      st.session_state.deck = st.session_state.discard_pile
      st.session_state.discard_pile = []
      random.shuffle(st.session_state.deck)
  if st.session_state.deck:
    return st.session_state.deck.pop()
  return None


if "player_hp" not in st.session_state:
  init_game()

# タイトル
st.title("💻 スート・コード：ネットワーク [拡張版]")
st.markdown(
    "**サイバーパンク・ハッキングバトル** — 複数カード同時選択によるコンボと資金調達戦で敵メインフレームを圧倒せよ！"
)

# ステータス表示
col1, col2, col3 = st.columns(3)
with col1:
  st.metric(
      label="プレイヤー サーバー耐久 (HP)",
      value=f"{st.session_state.player_hp} / 100",
  )
  st.metric(
      label="プレイヤー資金 (Credits)", value=f"{st.session_state.player_credits} ⚡"
  )
with col2:
  st.markdown(f"<h3 style='text-align: center;'>TURN {st.session_state.turn}</h3>", unsafe_allow_html=True)
  st.markdown(f"<p style='text-align: center; color: gray;'>山札残り: {len(st.session_state.deck)}枚 ｜ 捨て札: {len(st.session_state.discard_pile)}枚</p>", unsafe_allow_html=True)
with col3:
  st.metric(
      label="CPU サーバー耐久 (HP)", value=f"{st.session_state.cpu_hp} / 100"
  )
  st.metric(label="CPU資金 (Credits)", value=f"{st.session_state.cpu_credits} ⚡")

st.divider()

# 勝敗判定（HP枯渇 または 資金差など）
if st.session_state.player_hp <= 0 or st.session_state.cpu_hp <= 0:
  st.session_state.game_over = True
  if st.session_state.player_hp <= 0 and st.session_state.cpu_hp <= 0:
    # 両者同時HP切れの場合は資金勝負
    if st.session_state.player_credits >= st.session_state.cpu_credits:
      st.session_state.winner = "プレイヤー"
    else:
      st.session_state.winner = "CPU"
  elif st.session_state.player_hp <= 0:
    st.session_state.winner = "CPU"
  else:
    st.session_state.winner = "プレイヤー"

if st.session_state.game_over:
  if st.session_state.winner == "プレイヤー":
    st.balloons()
    st.success(f"🎉 ハッキング勝利！ 敵を制圧しました！（最終資金: プレイヤー {st.session_state.player_credits} ⚡ vs CPU {st.session_state.cpu_credits} ⚡）")
  else:
    st.error(f"💥 ハッキング失敗… システムがロックアウトされました。（最終資金: プレイヤー {st.session_state.player_credits} ⚡ vs CPU {st.session_state.cpu_credits} ⚡）")

  if st.button("🔄 システム再起動 (リトライ)"):
    init_game()
    st.rerun()
  st.stop()


# --- プレイヤーターン：複数カード選択 ---
st.subheader("🃏 サイバーデッキ（手札ターミナル・複数選択可能）")
st.markdown("戦術に合わせて複数のプロトコルを同時に選択し、強力なコンボを発動せよ。")

# 手札の選択肢マップ作成
hand_options = {
    f"[{c['id']}] 属性: {c['suit']} ｜ 値: {c['val']} (インデックス:{i})": i
    for i, c in enumerate(st.session_state.player_hand)
}

selected_labels = st.multiselect(
    "同時に実行するカードを選択してください:",
    options=list(hand_options.keys()),
    max_selections=3  # 最大3枚まで同時選択可能
)

selected_indices = [hand_options[label] for label in selected_labels]

# 選択されたカードの一覧表示
if selected_indices:
  st.markdown("#### ⚡ 選択中のコマンドプレビュー")
  preview_cols = st.columns(len(selected_indices))
  for idx, card_i in enumerate(selected_indices):
    c = st.session_state.player_hand[card_i]
    with preview_cols[idx]:
      try:
        st.image(c["img"], width=200, caption=f"{c['id']}")
      except Exception:
        st.markdown(f"**{c['id']}**")
      st.text(f"属性:{c['suit']} / 値:{c['val']}")
else:
  st.info("💡 カードを1枚以上選択すると、コンボ効果や詳細を確認できます。")

st.divider()

# ターン実行ボタン
if st.button("🚀 選択したカードで一斉ハッキングを実行", type="primary", disabled=len(selected_indices) == 0):
  
  # コンボ計算用の集計
  suits_played = [st.session_state.player_hand[i]['suit'] for i in selected_indices]
  vals_played = [st.session_state.player_hand[i]['val'] for i in selected_indices]
  
  # 同ースートの数、同数字のペア数をカウント
  suit_counts = {s: suits_played.count(s) for s in set(suits_played)}
  val_counts = {v: vals_played.count(v) for v in set(vals_played)}
  
  # ボーナス倍率の決定
  # 同スートが複数あればボーナス
  max_same_suit = max(suit_counts.values()) if suit_counts else 1
  suit_multiplier = 1.5 if max_same_suit >= 2 else 1.0
  if max_same_suit >= 3:
    suit_multiplier = 2.0

  # 同数字（ペア）があれば追加ボーナス
  has_number_pair = any(v >= 2 for v in val_counts.values())

  total_damage = 0
  total_heal = 0
  total_credits = 0

  # 各カードの効果処理
  # 選択されたインデックスが大きい順（後ろから）popするために降順ソート
  sorted_indices = sorted(selected_indices, reverse=True)

  for card_i in sorted_indices:
    card = st.session_state.player_hand[card_i]
    
    if card["type"] == "normal":
      if card["suit"] == "♣":  # ウイルス攻撃
        dmg = int(card["val"] * 2 * suit_multiplier)
        total_damage += dmg
      elif card["suit"] == "♠":  # 防御
        hf = int(card["val"] * 2 * suit_multiplier)
        total_heal += hf
      elif card["suit"] == "♥":  # 修復
        hf = int(card["val"] * 1.5 * suit_multiplier)
        total_heal += hf
      elif card["suit"] == "♦":  # 資金獲得
        cr = int(card["val"] * suit_multiplier)
        total_credits += cr

    elif card["type"] == "bug":  # バグカード
      effect_type = random.choice(["self_damage", "big_attack", "credit_boost"])
      if effect_type == "self_damage":
        st.session_state.player_hp -= 10
        st.toast("⚠️ バグ発生！ 10ダメージを受けた。", icon="💥")
      elif effect_type == "big_attack":
        total_damage += 30
      else:
        total_credits += 15

    elif card["type"] == "ai":  # AIカード
      total_damage += 25
      total_heal += 15
      total_credits += 10

    # 使用したカードを手札から除外し、捨て札置き場へ移動
    used_card = st.session_state.player_hand.pop(card_i)
    st.session_state.discard_pile.append(used_card)

  # ペアボーナス適用
  if has_number_pair:
    total_damage += 15
    total_credits += 10
    st.toast("✨【ペア・コンボ発動】同数字の共鳴により追加効果が発生！", icon="🔥")

  if max_same_suit >= 2:
    st.toast(f"🌊【スート・シナジー】同属性の同期により効果が {suit_multiplier}倍 に増幅！", icon="⚡")

  # 反映
  if total_damage > 0:
    st.session_state.cpu_hp = max(0, st.session_state.cpu_hp - total_damage)
    st.toast(f"ウイルス攻撃成功！ CPUに {total_damage} のダメージ！", icon="🦠")
  if total_heal > 0:
    st.session_state.player_hp = min(100, st.session_state.player_hp + total_heal)
    st.toast(f"システムが強化・修復され、HPが {total_heal} 回復！", icon="🛡️")
  if total_credits > 0:
    st.session_state.player_credits += total_credits
    st.toast(f"暗号通貨を大量調達！ +{total_credits} ⚡", icon="💠")

  # 足りた枚数分、新しいカードを補充
  cards_to_draw = len(selected_indices)
  for _ in range(cards_to_draw):
    new_c = draw_card_for_player()
    if new_c:
      st.session_state.player_hand.append(new_c)

  # --- CPUのターン処理 ---
  if st.session_state.cpu_hp > 0 and st.session_state.cpu_hand:
    cpu_card_idx = random.randint(0, len(st.session_state.cpu_hand) - 1)
    cpu_card = st.session_state.cpu_hand.pop(cpu_card_idx)
    st.session_state.discard_pile.append(cpu_card)

    if cpu_card["type"] == "normal":
      if cpu_card["suit"] == "♣":
        cpu_dmg = cpu_card["val"] * 2
        st.session_state.player_hp = max(0, st.session_state.player_hp - cpu_dmg)
        st.toast(f"敵(CPU)の反撃！ ウイルス攻撃で {cpu_dmg} のダメージ！", icon="🚨")
      elif cpu_card["suit"] == "♦":
        cpu_cr = cpu_card["val"]
        st.session_state.cpu_credits += cpu_cr
        st.toast(f"敵(CPU)が暗号資産を調達 (+{cpu_cr} ⚡)", icon="💰")
      else:
        cpu_heal = cpu_card["val"]
        st.session_state.cpu_hp = min(100, st.session_state.cpu_hp + cpu_heal)
        st.toast(f"敵(CPU)がシステムを修復しました。", icon="🔧")
    else:
      st.session_state.player_hp = max(0, st.session_state.player_hp - 15)
      st.session_state.cpu_credits += 10
      st.toast("敵(CPU)が特殊AIコマンドを発動！", icon="⚠️")

    new_cpu_c = draw_card_for_cpu()
    if new_cpu_c:
      st.session_state.cpu_hand.append(new_cpu_c)

  st.session_state.turn += 1
  st.rerun()
