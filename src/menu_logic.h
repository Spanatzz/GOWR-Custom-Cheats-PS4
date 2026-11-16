#ifndef GOWR_MENU_LOGIC_H
#define GOWR_MENU_LOGIC_H
#include <stdint.h>
/* Modelo de entrada neutral, NO equivale a un hook instalado en PS4. */
enum MenuButton {
  BTN_L1 = 1u<<0, BTN_CIRCLE = 1u<<1, BTN_UP = 1u<<2,
  BTN_DOWN = 1u<<3, BTN_CROSS = 1u<<4, BTN_L2 = 1u<<5, BTN_R2 = 1u<<6
};
enum { MENU_CATEGORIES=4, MENU_ITEMS=10 };
typedef struct {
  int opened;
  int category;
  int selected;
  int toggles[MENU_ITEMS];
  uint32_t previous;
  int combo_latched;
} MenuState;
void menu_init(MenuState *m);
/* Procesa botones de una muestra; requiere adaptador ScePadData y renderer de overlay. */
void menu_update(MenuState *m, uint32_t buttons);
#endif
