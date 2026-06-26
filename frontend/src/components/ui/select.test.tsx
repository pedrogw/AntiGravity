import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from './select';

describe('Select', () => {
  it('deve mostrar placeholder quando nenhum valor selecionado', () => {
    render(
      <Select value="" onValueChange={vi.fn()}>
        <SelectTrigger>
          <SelectValue placeholder="Escolha um item" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="1">Item Um</SelectItem>
        </SelectContent>
      </Select>,
    );
    expect(screen.getByText('Escolha um item')).toBeInTheDocument();
  });

  it('deve mostrar label do item selecionado em vez do value bruto', () => {
    render(
      <Select value="1" onValueChange={vi.fn()}>
        <SelectTrigger>
          <SelectValue placeholder="Escolha" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="1">Item Um</SelectItem>
        </SelectContent>
      </Select>,
    );
    const trigger = screen.getByRole('button');
    expect(trigger).toHaveTextContent('Item Um');
    expect(screen.queryByText('1')).not.toBeInTheDocument();
  });

  it('deve atualizar label ao mudar o valor selecionado', () => {
    const { rerender } = render(
      <Select value="1" onValueChange={vi.fn()}>
        <SelectTrigger>
          <SelectValue placeholder="Escolha" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="1">Item Um</SelectItem>
          <SelectItem value="2">Item Dois</SelectItem>
        </SelectContent>
      </Select>,
    );
    const trigger = screen.getByRole('button');
    expect(trigger).toHaveTextContent('Item Um');

    rerender(
      <Select value="2" onValueChange={vi.fn()}>
        <SelectTrigger>
          <SelectValue placeholder="Escolha" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="1">Item Um</SelectItem>
          <SelectItem value="2">Item Dois</SelectItem>
        </SelectContent>
      </Select>,
    );
    expect(trigger).toHaveTextContent('Item Dois');
  });

  it('deve chamar onValueChange com o value ao selecionar item', () => {
    const onValueChange = vi.fn();
    render(
      <Select value="" onValueChange={onValueChange}>
        <SelectTrigger>
          <SelectValue placeholder="Escolha" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="1">Item Um</SelectItem>
        </SelectContent>
      </Select>,
    );

    fireEvent.click(screen.getByRole('button', { name: /escolha/i }));
    fireEvent.click(screen.getByText('Item Um'));
    expect(onValueChange).toHaveBeenCalledWith('1');
  });
});
