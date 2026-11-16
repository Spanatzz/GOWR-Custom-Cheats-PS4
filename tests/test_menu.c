#include <assert.h>
#include <stdio.h>
#include "../src/menu_logic.h"
int main(void) {
  MenuState m; menu_init(&m);
  assert(!m.opened);
  menu_update(&m, BTN_L1 | BTN_CIRCLE);
  assert(m.opened);
  menu_update(&m, BTN_L1 | BTN_CIRCLE);
  assert(m.opened); /* no repetir */
  menu_update(&m, 0);
  menu_update(&m, BTN_L1 | BTN_CIRCLE);
  assert(!m.opened); /* cierre */
  menu_update(&m, 0);
  menu_update(&m, BTN_L1 | BTN_CIRCLE);
  assert(m.opened);
  menu_update(&m, 0);
  menu_update(&m, BTN_CROSS);
  assert(m.toggles[0]); /* maestro */
  menu_update(&m, 0);
  menu_update(&m, BTN_DOWN);
  menu_update(&m, 0);
  menu_update(&m, BTN_CROSS);
  assert(m.toggles[1]);
  menu_update(&m, 0);
  menu_update(&m, BTN_UP);
  menu_update(&m, 0);
  menu_update(&m, BTN_CROSS);
  assert(!m.toggles[0] && !m.toggles[1]);
  puts("OK - lógica L1+O, navegación y maestro");
  return 0;
}
